
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database import get_db
from backend.models.loan_application import LoanApplication
from backend.models.applicant import Applicant
from backend.models.loan_product import LoanProduct
from backend.schemas.loan_application import (
    LoanApplicationCreate,
    LoanApplicationResponse
)

router = APIRouter(
    prefix="/api/applications",
    tags=["Loan Applications"]
)


@router.post("/", response_model=LoanApplicationResponse, status_code=201)
def create_application(
    application_data: LoanApplicationCreate,
    db: Session = Depends(get_db)
):
    applicant = db.query(Applicant).filter(
        Applicant.applicant_id == application_data.applicant_id
    ).first()

    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    product = db.query(LoanProduct).filter(
        LoanProduct.product_id == application_data.product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Loan product not found")

    application = LoanApplication(**application_data.model_dump())

    try:
        db.add(application)
        db.commit()
        db.refresh(application)
        return application

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Application ID already exists"
        )


@router.get("/", response_model=list[LoanApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    return db.query(LoanApplication).order_by(
        LoanApplication.submitted_at.desc()
    ).limit(100).all()


@router.get("/{application_id}", response_model=LoanApplicationResponse)
def get_application(application_id: str, db: Session = Depends(get_db)):
    application = db.query(LoanApplication).filter(
        LoanApplication.application_id == application_id
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    return application
