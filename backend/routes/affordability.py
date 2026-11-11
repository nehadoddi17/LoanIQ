
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db

from backend.models.loan_application import LoanApplication
from backend.models.loan_product import LoanProduct
from backend.models.income_source import IncomeSource
from backend.models.credit_facility import CreditFacility
from backend.models.affordability_check import AffordabilityCheck

from backend.services.affordability import calculate_affordability
from backend.schemas.affordability import AffordabilityResponse


router = APIRouter(
    prefix="/api/affordability",
    tags=["Affordability"]
)


@router.post(
    "/{application_id}/calculate",
    response_model=AffordabilityResponse
)
def run_affordability_check(
    application_id: str,
    db: Session = Depends(get_db)
):
    # 1. Find application.
    application = db.query(LoanApplication).filter(
        LoanApplication.application_id == application_id
    ).first()

    if not application:
        raise HTTPException(404, "Loan application not found")

    # 2. Find selected product.
    product = db.query(LoanProduct).filter(
        LoanProduct.product_id == application.product_id
    ).first()

    if not product:
        raise HTTPException(404, "Loan product not found")

    # 3. Retrieve financial information.
    income_sources = db.query(IncomeSource).filter(
        IncomeSource.applicant_id == application.applicant_id
    ).all()

    credit_facilities = db.query(CreditFacility).filter(
        CreditFacility.applicant_id == application.applicant_id
    ).all()

    # 4. Calculate affordability.
    try:
        result = calculate_affordability(
            application,
            product,
            income_sources,
            credit_facilities
        )
    except ValueError as exc:
        raise HTTPException(422, str(exc))

    # 5. Generate a sequential check ID for this application.
    existing_count = db.query(AffordabilityCheck).filter(
        AffordabilityCheck.application_id == application_id
    ).count()

    check_id = f"CHK-{application_id}-{existing_count + 1:03d}"

    # 6. Save the result.
    check = AffordabilityCheck(
        check_id=check_id,
        application_id=application_id,
        **result
    )

    db.add(check)
    db.commit()
    db.refresh(check)

    return check


@router.get(
    "/{application_id}",
    response_model=list[AffordabilityResponse]
)
def get_affordability_checks(
    application_id: str,
    db: Session = Depends(get_db)
):
    application = db.query(LoanApplication).filter(
        LoanApplication.application_id == application_id
    ).first()

    if not application:
        raise HTTPException(404, "Loan application not found")

    return db.query(AffordabilityCheck).filter(
        AffordabilityCheck.application_id == application_id
    ).order_by(AffordabilityCheck.checked_at.desc()).all()
