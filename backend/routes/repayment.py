
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db

from backend.models.loan_application import LoanApplication
from backend.models.loan_product import LoanProduct
from backend.models.repayment_schedule import RepaymentSchedule
from backend.models.repayment_installment import RepaymentInstallment
from backend.models.loan_decision import LoanDecision

from backend.services.repayment import generate_repayment_schedule
from backend.schemas.repayment import (
    RepaymentScheduleResponse,
    InstallmentResponse
)

router = APIRouter(
    prefix="/api/repayments",
    tags=["Repayment Schedules"]
)


@router.post(
    "/{application_id}/generate",
    response_model=RepaymentScheduleResponse,
    status_code=201
)
def create_repayment_schedule(
    application_id: str,
    db: Session = Depends(get_db)
):
    application = db.query(LoanApplication).filter(
        LoanApplication.application_id == application_id
    ).with_for_update().first()

    if not application:
        raise HTTPException(404, "Loan application not found")

    latest_decision = db.query(LoanDecision).filter(
        LoanDecision.application_id == application_id
    ).order_by(LoanDecision.decision_at.desc()).first()

    if not latest_decision or latest_decision.decision != "APPROVED":
        raise HTTPException(
            409,
            "Only applications with a latest APPROVED decision can generate schedules"
        )

    existing_schedule = db.query(RepaymentSchedule).filter(
        RepaymentSchedule.application_id == application_id
    ).first()

    if existing_schedule:
        raise HTTPException(
            409,
            "Repayment schedule already exists for this application"
        )

    product = db.query(LoanProduct).filter(
        LoanProduct.product_id == application.product_id
    ).first()

    if not product:
        raise HTTPException(404, "Loan product not found")

    try:
        result = generate_repayment_schedule(
            principal=application.requested_amount,
            annual_interest_rate=product.annual_interest_rate,
            tenure_months=application.requested_term_months
        )

        schedule_id = f"SCH-{uuid4().hex[:20]}"

        schedule = RepaymentSchedule(
            schedule_id=schedule_id,
            application_id=application_id,
            principal_amount=result["principal_amount"],
            total_interest=result["total_interest"],
            total_payable=result["total_payable"],
            expected_installment_count=result["expected_installment_count"],
            calculated_installment_total=result["calculated_installment_total"],
            reconciliation_status=result["reconciliation_status"]
        )

        db.add(schedule)
        db.flush()

        for item in result["installments"]:
            installment = RepaymentInstallment(
                installment_id=f"INS-{uuid4().hex[:20]}",
                schedule_id=schedule_id,
                installment_number=item["installment_number"],
                due_date=item["due_date"],
                principal_component=item["principal_component"],
                interest_component=item["interest_component"],
                installment_amount=item["installment_amount"],
                payment_status="PENDING"
            )
            db.add(installment)

        if result["reconciliation_status"] != "RECONCILED":
            raise HTTPException(
                422,
                "Repayment schedule failed reconciliation"
            )

        db.commit()
        db.refresh(schedule)

        return schedule

    except ValueError as exc:
        db.rollback()
        raise HTTPException(422, str(exc))

    except Exception:
        db.rollback()
        raise


@router.get(
    "/{application_id}",
    response_model=RepaymentScheduleResponse
)
def get_repayment_schedule(
    application_id: str,
    db: Session = Depends(get_db)
):
    schedule = db.query(RepaymentSchedule).filter(
        RepaymentSchedule.application_id == application_id
    ).first()

    if not schedule:
        raise HTTPException(404, "Repayment schedule not found")

    return schedule


@router.get(
    "/{application_id}/installments",
    response_model=list[InstallmentResponse]
)
def get_installments(
    application_id: str,
    db: Session = Depends(get_db)
):
    schedule = db.query(RepaymentSchedule).filter(
        RepaymentSchedule.application_id == application_id
    ).first()

    if not schedule:
        raise HTTPException(404, "Repayment schedule not found")

    return db.query(RepaymentInstallment).filter(
        RepaymentInstallment.schedule_id == schedule.schedule_id
    ).order_by(RepaymentInstallment.installment_number).all()
