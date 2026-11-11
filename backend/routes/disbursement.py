
from uuid import uuid4
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db

from backend.models.loan_application import LoanApplication
from backend.models.loan_decision import LoanDecision
from backend.models.repayment_schedule import RepaymentSchedule
from backend.models.disbursement import Disbursement

from backend.schemas.disbursement import DisbursementResponse


router = APIRouter(
    prefix="/api/disbursements",
    tags=["Disbursements"]
)


@router.post(
    "/{application_id}/execute",
    response_model=DisbursementResponse,
    status_code=201
)
def execute_disbursement(
    application_id: str,
    db: Session = Depends(get_db)
):
    # Lock the application row to serialize disbursement attempts.
    application = db.query(LoanApplication).filter(
        LoanApplication.application_id == application_id
    ).with_for_update().first()

    if not application:
        raise HTTPException(404, "Loan application not found")

    # Check the latest decision.
    latest_decision = db.query(LoanDecision).filter(
        LoanDecision.application_id == application_id
    ).order_by(LoanDecision.decision_at.desc()).first()

    if not latest_decision or latest_decision.decision != "APPROVED":
        raise HTTPException(
            409,
            "Only approved applications can be disbursed"
        )

    # Check repayment schedule.
    schedule = db.query(RepaymentSchedule).filter(
        RepaymentSchedule.application_id == application_id
    ).first()

    if not schedule:
        raise HTTPException(
            409,
            "Repayment schedule has not been generated"
        )

    if schedule.reconciliation_status != "RECONCILED":
        raise HTTPException(
            409,
            "Repayment schedule is not reconciled"
        )

    # Prevent duplicate disbursement.
    existing = db.query(Disbursement).filter(
        Disbursement.application_id == application_id
    ).first()

    if existing:
        raise HTTPException(
            409,
            "Disbursement already exists for this application"
        )

    # Create a simulated disbursement record.
    record = Disbursement(
        disbursement_id=f"DIS-{uuid4().hex[:20]}",
        application_id=application_id,
        amount=application.requested_amount,
        disbursement_status="DISBURSED",
        disbursed_at=datetime.utcnow(),
        transaction_reference=f"DEMO-TXN-{uuid4().hex[:12].upper()}"
    )

    try:
        db.add(record)
        application.application_status = "DISBURSED"

        db.commit()
        db.refresh(record)

        return record

    except Exception:
        db.rollback()
        raise


@router.get(
    "/{application_id}",
    response_model=list[DisbursementResponse]
)
def get_disbursements(
    application_id: str,
    db: Session = Depends(get_db)
):
    application = db.query(LoanApplication).filter(
        LoanApplication.application_id == application_id
    ).first()

    if not application:
        raise HTTPException(404, "Loan application not found")

    return db.query(Disbursement).filter(
        Disbursement.application_id == application_id
    ).all()
