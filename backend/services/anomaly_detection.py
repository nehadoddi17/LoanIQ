
from collections import defaultdict
from decimal import Decimal
from datetime import datetime
from hashlib import sha256

from sqlalchemy.orm import Session

from backend.models.loan_application import LoanApplication
from backend.models.loan_product import LoanProduct
from backend.models.loan_decision import LoanDecision
from backend.models.affordability_check import AffordabilityCheck
from backend.models.application_document import ApplicationDocument
from backend.models.income_source import IncomeSource
from backend.models.repayment_schedule import RepaymentSchedule
from backend.models.repayment_installment import RepaymentInstallment
from backend.models.disbursement import Disbursement
from backend.models.anomaly_case import AnomalyCase


REQUIRED_DOCUMENTS = {
    "ID_PROOF",
    "ADDRESS_PROOF",
    "BANK_STATEMENT",
    "INCOME_PROOF"
}

ANOMALY_TYPES = {
    "INVALID_LOAN_TENURE",
    "SCHEDULE_RECONCILIATION_MISMATCH",
    "DECISION_BEFORE_REQUIRED_CHECKS",
    "INCOME_SOURCE_CONFLICT",
    "DUPLICATE_DISBURSEMENT"
}


def make_anomaly_id(application_id: str, anomaly_type: str) -> str:
    """Create a stable ID so repeated scans do not duplicate findings."""
    raw = f"{application_id}:{anomaly_type}"
    digest = sha256(raw.encode("utf-8")).hexdigest()[:24]
    return f"ANM-{digest}"


def detect_invalid_tenure(application, product):
    if not product:
        return None

    if not (
        product.min_term_months
        <= application.requested_term_months
        <= product.max_term_months
    ):
        return (
            "INVALID_LOAN_TENURE",
            (
                f"Requested tenure is {application.requested_term_months} months; "
                f"product permits {product.min_term_months} to "
                f"{product.max_term_months} months."
            )
        )

    return None


def detect_schedule_mismatch(db: Session, application_id: str):
    schedule = db.query(RepaymentSchedule).filter(
        RepaymentSchedule.application_id == application_id
    ).first()

    if not schedule:
        return None

    installments = db.query(RepaymentInstallment).filter(
        RepaymentInstallment.schedule_id == schedule.schedule_id
    ).all()

    actual_count = len(installments)

    actual_total = sum(
        (Decimal(str(item.installment_amount or 0)) for item in installments),
        Decimal("0")
    )

    expected_total = Decimal(str(schedule.total_payable or 0))
    stored_total = Decimal(str(schedule.calculated_installment_total or 0))

    tolerance = Decimal("0.01")

    count_mismatch = (
        schedule.expected_installment_count is not None
        and actual_count != schedule.expected_installment_count
    )

    total_mismatch = (
        abs(actual_total - expected_total) > tolerance
        or abs(stored_total - expected_total) > tolerance
    )

    status_mismatch = schedule.reconciliation_status != "RECONCILED"

    if count_mismatch or total_mismatch or status_mismatch:
        return (
            "SCHEDULE_RECONCILIATION_MISMATCH",
            (
                f"Schedule {schedule.schedule_id}: expected "
                f"{schedule.expected_installment_count} installments, "
                f"found {actual_count}; expected payable "
                f"{expected_total}, actual installment total "
                f"{actual_total}; reconciliation status "
                f"{schedule.reconciliation_status}."
            )
        )

    return None


def detect_decision_before_checks(db: Session, application_id: str):
    decisions = db.query(LoanDecision).filter(
        LoanDecision.application_id == application_id,
        LoanDecision.decision == "APPROVED"
    ).all()

    if not decisions:
        return None

    documents = db.query(ApplicationDocument).filter(
        ApplicationDocument.application_id == application_id
    ).all()

    affordability_checks = db.query(AffordabilityCheck).filter(
        AffordabilityCheck.application_id == application_id
    ).all()

    for decision in decisions:
        decision_time = decision.decision_at

        # An approval without an affordability check is a workflow anomaly.
        valid_affordability = any(
            check.checked_at is not None
            and decision_time is not None
            and check.checked_at <= decision_time
            and check.check_status == "PASS"
            for check in affordability_checks
        )

        verified_before_decision = {
            doc.document_type.upper()
            for doc in documents
            if doc.document_type
            and doc.verification_status == "VERIFIED"
            and doc.verified_at is not None
            and decision_time is not None
            and doc.verified_at <= decision_time
        }

        missing_at_decision = REQUIRED_DOCUMENTS - verified_before_decision

        if not valid_affordability or missing_at_decision:
            reasons = []

            if not valid_affordability:
                reasons.append(
                    "No PASS affordability check existed before approval"
                )

            if missing_at_decision:
                reasons.append(
                    "Required documents not verified before approval: "
                    + ", ".join(sorted(missing_at_decision))
                )

            return (
                "DECISION_BEFORE_REQUIRED_CHECKS",
                f"Decision {decision.decision_id}: " + "; ".join(reasons)
            )

    return None


def detect_income_conflict(db: Session, applicant_id: str):
    records = db.query(IncomeSource).filter(
        IncomeSource.applicant_id == applicant_id
    ).all()

    grouped = defaultdict(list)

    for record in records:
        key = (
            (record.source_type or "").strip().upper(),
            (record.source_name or "").strip().casefold()
        )

        if key != ("", ""):
            grouped[key].append(record)

    conflicts = []

    for key, items in grouped.items():
        amounts = {
            Decimal(str(item.monthly_amount or 0)).quantize(
                Decimal("0.01")
            )
            for item in items
        }

        if len(amounts) > 1:
            conflicts.append(
                f"{key[0]} / {key[1]} has conflicting monthly amounts: "
                + ", ".join(str(amount) for amount in sorted(amounts))
            )

    if conflicts:
        return (
            "INCOME_SOURCE_CONFLICT",
            "Conflicting records for the same income source: "
            + "; ".join(conflicts)
        )

    return None


def detect_duplicate_disbursement(db: Session, application_id: str):
    records = db.query(Disbursement).filter(
        Disbursement.application_id == application_id,
        Disbursement.disbursement_status == "DISBURSED"
    ).all()

    if len(records) > 1:
        ids = ", ".join(record.disbursement_id for record in records)

        return (
            "DUPLICATE_DISBURSEMENT",
            f"{len(records)} successful disbursement records found: {ids}"
        )

    return None


def detect_application_anomalies(db: Session, application):
    findings = []

    product = db.query(LoanProduct).filter(
        LoanProduct.product_id == application.product_id
    ).first()

    applicant_id = application.applicant_id

    # Rule 1: Requested loan tenure outside product limits.
    finding = detect_invalid_tenure(application, product)
    if finding:
        findings.append(finding)

    # Rule 2: Repayment schedule reconciliation mismatch.
    finding = detect_schedule_mismatch(db, application.application_id)
    if finding:
        findings.append(finding)

    # Rule 3: Approval before required checks.
    finding = detect_decision_before_checks(db, application.application_id)
    if finding:
        findings.append(finding)

    # Rule 4: Conflicting records for the same income source.
    finding = detect_income_conflict(db, applicant_id)
    if finding:
        findings.append(finding)

    # Rule 5: Multiple successful disbursements.
    finding = detect_duplicate_disbursement(db, application.application_id)
    if finding:
        findings.append(finding)

    return findings



def run_anomaly_detection(db: Session):
    applications = db.query(LoanApplication).all()

    total_detected = 0
    results = []

    # Track all anomalies found in this scan
    active_anomaly_ids = set()

    for application in applications:
        findings = detect_application_anomalies(db, application)

        for anomaly_type, description in findings:
            anomaly_id = make_anomaly_id(
                application.application_id,
                anomaly_type
            )

            active_anomaly_ids.add(anomaly_id)

            existing = db.query(AnomalyCase).filter(
                AnomalyCase.anomaly_id == anomaly_id
            ).first()

            if existing:
                existing.detected = True
                existing.description = description
                existing.detected_at = datetime.utcnow()
            else:
                record = AnomalyCase(
                    anomaly_id=anomaly_id,
                    application_id=application.application_id,
                    anomaly_type=anomaly_type,
                    description=description,
                    detected=True,
                    detected_at=datetime.utcnow()
                )
                db.add(record)

            total_detected += 1

            results.append({
                "application_id": application.application_id,
                "anomaly_type": anomaly_type,
                "description": description
            })

    # Mark previously detected anomalies as resolved
    previous_cases = db.query(AnomalyCase).filter(
        AnomalyCase.detected == True
    ).all()

    for case in previous_cases:
        if case.anomaly_id not in active_anomaly_ids:
            case.detected = False

    db.commit()

    return {
        "applications_scanned": len(applications),
        "anomalies_detected": total_detected,
        "findings": results
    }

