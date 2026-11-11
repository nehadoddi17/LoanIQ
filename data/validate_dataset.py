
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "generated"

EXPECTED_ANOMALY_TYPES = {
    "INVALID_LOAN_TENURE",
    "SCHEDULE_RECONCILIATION_MISMATCH",
    "DECISION_BEFORE_REQUIRED_CHECKS",
    "INCOME_SOURCE_CONFLICT",
    "DUPLICATE_DISBURSEMENT",
}

ANOMALY_CASES_PER_TYPE = 120
TOLERANCE = 0.01


def validate_dataset():
    print("=" * 65)
    print("LOANIQ DATASET VALIDATION")
    print("=" * 65)

    # ---------------------------------------------------------
    # LOAD DATA
    # ---------------------------------------------------------

    applicants = pd.read_csv(DATA_DIR / "applicants.csv")
    applications = pd.read_csv(DATA_DIR / "loan_applications.csv")
    products = pd.read_csv(DATA_DIR / "loan_products.csv")
    employment = pd.read_csv(DATA_DIR / "employment.csv")
    income = pd.read_csv(DATA_DIR / "income_sources.csv")
    facilities = pd.read_csv(DATA_DIR / "credit_facilities.csv")
    documents = pd.read_csv(DATA_DIR / "application_documents.csv")
    affordability = pd.read_csv(DATA_DIR / "affordability_checks.csv")
    decisions = pd.read_csv(DATA_DIR / "loan_decisions.csv")
    schedules = pd.read_csv(DATA_DIR / "repayment_schedules.csv")
    installments = pd.read_csv(DATA_DIR / "repayment_installments.csv")
    disbursements = pd.read_csv(DATA_DIR / "disbursements.csv")
    anomalies = pd.read_csv(DATA_DIR / "anomaly_cases.csv")
    ground_truth = pd.read_csv(DATA_DIR / "ground_truth.csv")

    checks = []

    def check(name, condition):
        checks.append((name, bool(condition)))

    # ---------------------------------------------------------
    # 1. RECORD COUNTS
    # ---------------------------------------------------------

    check("10,000 applicants", len(applicants) == 10000)
    check("6,000 applications", len(applications) == 6000)
    check("4 loan products", len(products) == 4)
    check("10,000 employment records", len(employment) == 10000)
    check("10,120 income records", len(income) == 10120)
    check("6,000 credit facilities", len(facilities) == 6000)
    check("24,000 application documents", len(documents) == 24000)
    check("6,000 affordability checks", len(affordability) == 6000)
    check("6,000 loan decisions", len(decisions) == 6000)
    check("6,000 repayment schedules", len(schedules) == 6000)
    check("6,000 disbursement applications have records",
          len(disbursements) == 6120)
    check("600 anomaly cases", len(anomalies) == 600)
    check("600 ground truth labels", len(ground_truth) == 600)

    # ---------------------------------------------------------
    # 2. PRIMARY KEY UNIQUENESS
    # ---------------------------------------------------------

    primary_keys = [
        (applicants, "applicant_id", "Applicant"),
        (applications, "application_id", "Application"),
        (products, "product_id", "Product"),
        (employment, "employment_id", "Employment"),
        (income, "income_source_id", "Income source"),
        (facilities, "facility_id", "Credit facility"),
        (documents, "document_id", "Document"),
        (affordability, "check_id", "Affordability check"),
        (decisions, "decision_id", "Decision"),
        (schedules, "schedule_id", "Schedule"),
        (installments, "installment_id", "Installment"),
        (disbursements, "disbursement_id", "Disbursement"),
        (anomalies, "anomaly_id", "Anomaly"),
        (ground_truth, "ground_truth_id", "Ground truth"),
    ]

    for dataframe, column, label in primary_keys:
        check(
            f"{label} IDs unique",
            dataframe[column].is_unique
        )

    # ---------------------------------------------------------
    # 3. FOREIGN KEY VALIDATION
    # ---------------------------------------------------------

    applicant_ids = set(applicants["applicant_id"])
    application_ids = set(applications["application_id"])
    product_ids = set(products["product_id"])
    schedule_ids = set(schedules["schedule_id"])
    anomaly_ids = set(anomalies["anomaly_id"])

    check(
        "Application applicant references valid",
        set(applications["applicant_id"]).issubset(applicant_ids)
    )

    check(
        "Application product references valid",
        set(applications["product_id"]).issubset(product_ids)
    )

    check(
        "Employment applicant references valid",
        set(employment["applicant_id"]).issubset(applicant_ids)
    )

    check(
        "Income applicant references valid",
        set(income["applicant_id"]).issubset(applicant_ids)
    )

    check(
        "Credit facility applicant references valid",
        set(facilities["applicant_id"]).issubset(applicant_ids)
    )

    check(
        "Document application references valid",
        set(documents["application_id"]).issubset(application_ids)
    )

    check(
        "Affordability application references valid",
        set(affordability["application_id"]).issubset(application_ids)
    )

    check(
        "Decision application references valid",
        set(decisions["application_id"]).issubset(application_ids)
    )

    check(
        "Schedule application references valid",
        set(schedules["application_id"]).issubset(application_ids)
    )

    check(
        "Installment schedule references valid",
        set(installments["schedule_id"]).issubset(schedule_ids)
    )

    check(
        "Disbursement application references valid",
        set(disbursements["application_id"]).issubset(application_ids)
    )

    check(
        "Anomaly application references valid",
        set(anomalies["application_id"]).issubset(application_ids)
    )

    check(
        "Ground truth anomaly references valid",
        set(ground_truth["anomaly_id"]).issubset(anomaly_ids)
    )

    # ---------------------------------------------------------
    # 4. BASIC BUSINESS RULES
    # ---------------------------------------------------------

    check(
        "Requested loan amounts positive",
        (applications["requested_amount"] > 0).all()
    )

    check(
        "Credit scores within 300-900",
        applicants["credit_score"].between(300, 900).all()
    )

    check(
        "Monthly income positive",
        (income["monthly_amount"] > 0).all()
    )

    check(
        "Facility balances non-negative",
        (facilities["outstanding_balance"] >= 0).all()
    )

    check(
        "Affordability income positive",
        (affordability["monthly_income"] > 0).all()
    )

    check(
        "Decision values are APPROVED",
        (decisions["decision"] == "APPROVED").all()
    )

    check(
        "All disbursements have DISBURSED status",
        (disbursements["disbursement_status"] == "DISBURSED").all()
    )

    # ---------------------------------------------------------
    # 5. GROUND TRUTH VALIDATION
    # ---------------------------------------------------------

    check(
        "All five anomaly categories present",
        set(ground_truth["expected_anomaly_type"])
        == EXPECTED_ANOMALY_TYPES
    )

    check(
        "All ground truth labels are positive",
        (ground_truth["expected_anomaly"] == True).all()
    )

    anomaly_distribution = (
        ground_truth["expected_anomaly_type"].value_counts().to_dict()
    )

    for anomaly_type in EXPECTED_ANOMALY_TYPES:
        check(
            f"120 ground truth cases: {anomaly_type}",
            anomaly_distribution.get(anomaly_type, 0)
            == ANOMALY_CASES_PER_TYPE
        )

    # Ground truth and anomaly case must match.
    merged_gt = ground_truth.merge(
        anomalies,
        on="anomaly_id",
        how="left",
        suffixes=("_gt", "_case")
    )

    check(
        "Ground truth anomaly types match anomaly cases",
        (
            merged_gt["expected_anomaly_type"]
            == merged_gt["anomaly_type"]
        ).all()
    )

    # Verify that anomaly IDs follow the API's SHA256 algorithm.
    import hashlib

    expected_ids = anomalies.apply(
        lambda row: "ANM-" + hashlib.sha256(
            f"{row['application_id']}:{row['anomaly_type']}".encode("utf-8")
        ).hexdigest()[:24],
        axis=1
    )

    check(
        "Anomaly IDs match API SHA256 logic",
        (expected_ids == anomalies["anomaly_id"]).all()
    )

    # ---------------------------------------------------------
    # 6. ACTUAL ANOMALY CONDITION VALIDATION
    # ---------------------------------------------------------

    application_lookup = applications.merge(
        products,
        on="product_id",
        how="left"
    )

    invalid_tenure = application_lookup[
        (
            application_lookup["requested_term_months"]
            < application_lookup["min_term_months"]
        )
        |
        (
            application_lookup["requested_term_months"]
            > application_lookup["max_term_months"]
        )
    ]

    invalid_ids = set(invalid_tenure["application_id"])

    expected_invalid_ids = set(
        anomalies.loc[
            anomalies["anomaly_type"] == "INVALID_LOAN_TENURE",
            "application_id"
        ]
    )

    check(
        "120 genuine invalid tenure scenarios",
        len(invalid_ids) == 120
        and expected_invalid_ids.issubset(invalid_ids)
    )

    # Schedule mismatch: compare stored total with expected payable.
    schedule_mismatch = schedules[
        (
            (
                schedules["calculated_installment_total"]
                - schedules["total_payable"]
            ).abs() > TOLERANCE
        )
        |
        (schedules["reconciliation_status"] != "RECONCILED")
    ]

    mismatch_ids = set(schedule_mismatch["application_id"])

    expected_schedule_ids = set(
        anomalies.loc[
            anomalies["anomaly_type"]
            == "SCHEDULE_RECONCILIATION_MISMATCH",
            "application_id"
        ]
    )

    check(
        "120 genuine schedule mismatch scenarios",
        len(mismatch_ids) == 120
        and expected_schedule_ids.issubset(mismatch_ids)
    )

    # Decision before required checks:
    # Every scenario must lack a PASS affordability check before approval
    # and/or lack four verified documents before approval.
    premature_ids = set(
        anomalies.loc[
            anomalies["anomaly_type"]
            == "DECISION_BEFORE_REQUIRED_CHECKS",
            "application_id"
        ]
    )

    premature_valid = True

    required_documents = {
        "ID_PROOF",
        "ADDRESS_PROOF",
        "BANK_STATEMENT",
        "INCOME_PROOF",
    }

    for app_id in premature_ids:
        decision_rows = decisions[
            (decisions["application_id"] == app_id)
            & (decisions["decision"] == "APPROVED")
        ]

        if decision_rows.empty:
            premature_valid = False
            continue

        decision_time = pd.to_datetime(
            decision_rows.iloc[0]["decision_at"]
        )

        checks_for_app = affordability[
            affordability["application_id"] == app_id
        ].copy()

        checks_for_app["checked_at"] = pd.to_datetime(
            checks_for_app["checked_at"]
        )

        valid_pass = checks_for_app[
            (checks_for_app["check_status"] == "PASS")
            & (checks_for_app["checked_at"] <= decision_time)
        ]

        docs_for_app = documents[
            documents["application_id"] == app_id
        ].copy()

        docs_for_app["verified_at"] = pd.to_datetime(
            docs_for_app["verified_at"],
            errors="coerce"
        )

        verified_before = set(
            docs_for_app.loc[
                (docs_for_app["verification_status"] == "VERIFIED")
                & (docs_for_app["verified_at"] <= decision_time),
                "document_type"
            ].str.upper()
        )

        if (
            not valid_pass.empty
            and required_documents.issubset(verified_before)
        ):
            premature_valid = False

    check(
        "120 genuine premature approval scenarios",
        len(premature_ids) == 120 and premature_valid
    )

    # Income conflict: same applicant/source key with different amounts.
    conflict_ids = set(
        anomalies.loc[
            anomalies["anomaly_type"] == "INCOME_SOURCE_CONFLICT",
            "application_id"
        ]
    )

    conflict_applicant_ids = set(
        applications.loc[
            applications["application_id"].isin(conflict_ids),
            "applicant_id"
        ]
    )

    conflict_valid = True

    for applicant_id in conflict_applicant_ids:
        applicant_income = income[
            income["applicant_id"] == applicant_id
        ]

        grouped = applicant_income.groupby(
            [
                income["source_type"].str.strip().str.upper(),
                income["source_name"].str.strip().str.casefold(),
            ],
            dropna=False
        )["monthly_amount"].nunique()

        if not (grouped > 1).any():
            conflict_valid = False

    check(
        "120 genuine income conflict scenarios",
        len(conflict_ids) == 120 and conflict_valid
    )

    # Duplicate successful disbursements.
    successful = disbursements[
        disbursements["disbursement_status"] == "DISBURSED"
    ]

    duplicate_counts = successful.groupby(
        "application_id"
    ).size()

    duplicate_ids = set(
        duplicate_counts[duplicate_counts > 1].index
    )

    expected_duplicate_ids = set(
        anomalies.loc[
            anomalies["anomaly_type"] == "DUPLICATE_DISBURSEMENT",
            "application_id"
        ]
    )

    check(
        "120 genuine duplicate disbursement scenarios",
        len(duplicate_ids) == 120
        and expected_duplicate_ids.issubset(duplicate_ids)
    )

    # ---------------------------------------------------------
    # 7. REPAYMENT INSTALLMENT RECONCILIATION
    # ---------------------------------------------------------

    actual_installment_counts = installments.groupby(
        "schedule_id"
    ).size()

    expected_counts = schedules.set_index(
        "schedule_id"
    )["expected_installment_count"]

    counts_match = all(
        actual_installment_counts.get(schedule_id, 0) == expected_count
        for schedule_id, expected_count in expected_counts.items()
    )

    check(
        "Installment counts match schedule expectations",
        counts_match
    )

    actual_installment_totals = installments.groupby(
        "schedule_id"
    )["installment_amount"].sum()

    normal_schedules = schedules[
        schedules["reconciliation_status"] == "RECONCILED"
    ]

    normal_totals_match = True

    for _, schedule in normal_schedules.iterrows():
        actual_total = actual_installment_totals.get(
            schedule["schedule_id"], 0
        )

        if abs(actual_total - schedule["total_payable"]) > TOLERANCE:
            normal_totals_match = False
            break

    check(
        "Normal schedule installment totals reconcile",
        normal_totals_match
    )

    # ---------------------------------------------------------
    # 8. RESULTS
    # ---------------------------------------------------------

    print("\nVALIDATION RESULTS")
    print("-" * 65)

    passed = 0
    failed = 0

    for name, result in checks:
        if result:
            print(f"PASS: {name}")
            passed += 1
        else:
            print(f"FAIL: {name}")
            failed += 1

    print("-" * 65)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total checks: {len(checks)}")

    print("\nANOMALY DISTRIBUTION")
    for anomaly_type in sorted(EXPECTED_ANOMALY_TYPES):
        print(
            f"{anomaly_type}: "
            f"{anomaly_distribution.get(anomaly_type, 0)}"
        )

    if failed:
        raise SystemExit(
            "\nDataset validation failed. Review the failed checks."
        )

    print("\nALL DATASET VALIDATION CHECKS PASSED!")


if __name__ == "__main__":
    validate_dataset()
