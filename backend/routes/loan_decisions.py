
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.database import get_db

from backend.models.loan_application import LoanApplication
from backend.models.loan_product import LoanProduct
from backend.models.applicant import Applicant
from backend.models.application_document import ApplicationDocument
from backend.models.affordability_check import AffordabilityCheck
from backend.models.loan_decision import LoanDecision

from backend.services.decision_engine import evaluate_loan_application
from backend.schemas.loan_decision import LoanDecisionResponse


router = APIRouter(
    prefix="/api/decisions",
    tags=["Loan Decisions"]
)


@router.post(
    "/{application_id}/evaluate",
    response_model=LoanDecisionResponse,
    status_code=201
)
def evaluate_application(
    application_id: str,
    db: Session = Depends(get_db)
):
    # 1. Fetch application.
    application = db.query(LoanApplication).filter(
        LoanApplication.application_id == application_id
    ).first()

    if not application:
        raise HTTPException(404, "Loan application not found")

    # 2. Fetch applicant.
    applicant = db.query(Applicant).filter(
        Applicant.applicant_id == application.applicant_id
    ).first()

    if not applicant:
        raise HTTPException(404, "Applicant not found")

    # 3. Fetch loan product.
    product = db.query(LoanProduct).filter(
        LoanProduct.product_id == application.product_id
    ).first()

    if not product:
        raise HTTPException(404, "Loan product not found")

    # 4. Fetch application documents.
    documents = db.query(ApplicationDocument).filter(
        ApplicationDocument.application_id == application_id
    ).all()

    # 5. Fetch latest affordability check.
    affordability_check = db.query(AffordabilityCheck).filter(
        AffordabilityCheck.application_id == application_id
    ).order_by(
        desc(AffordabilityCheck.checked_at)
    ).first()

    # 6. Execute decision engine.
    result = evaluate_loan_application(
        application=application,
        product=product,
        applicant=applicant,
        documents=documents,
        affordability_check=affordability_check
    )

    # 7. Generate a unique decision ID.
    decision_id = f"DEC-{uuid4().hex[:20]}"

    # 8. Save decision history.
    decision_record = LoanDecision(
        decision_id=decision_id,
        application_id=application_id,
        decision=result["decision"],
        reason=result["reason"],
        decided_by="SYSTEM_RULE_ENGINE"
    )

    db.add(decision_record)

    # 9. Update application status.
    application.application_status = result["decision"]

    db.commit()
    db.refresh(decision_record)

    return decision_record


@router.get(
    "/{application_id}",
    response_model=list[LoanDecisionResponse]
)
def get_decision_history(
    application_id: str,
    db: Session = Depends(get_db)
):
    application = db.query(LoanApplication).filter(
        LoanApplication.application_id == application_id
    ).first()

    if not application:
        raise HTTPException(404, "Loan application not found")

    return db.query(LoanDecision).filter(
        LoanDecision.application_id == application_id
    ).order_by(
        desc(LoanDecision.decision_at)
    ).all()
