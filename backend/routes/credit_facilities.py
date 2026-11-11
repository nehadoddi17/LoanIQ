
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database import get_db
from backend.models.applicant import Applicant
from backend.models.credit_facility import CreditFacility
from backend.schemas.credit_facility import CreditFacilityCreate, CreditFacilityResponse

router = APIRouter(prefix="/api/credit-facilities", tags=["Credit Facilities"])


@router.post("/", response_model=CreditFacilityResponse, status_code=201)
def create_facility(data: CreditFacilityCreate, db: Session = Depends(get_db)):
    if not db.query(Applicant).filter(
        Applicant.applicant_id == data.applicant_id
    ).first():
        raise HTTPException(404, "Applicant not found")

    record = CreditFacility(**data.model_dump())
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Facility ID already exists")


@router.get("/{applicant_id}", response_model=list[CreditFacilityResponse])
def get_facilities(applicant_id: str, db: Session = Depends(get_db)):
    if not db.query(Applicant).filter(
        Applicant.applicant_id == applicant_id
    ).first():
        raise HTTPException(404, "Applicant not found")

    return db.query(CreditFacility).filter(
        CreditFacility.applicant_id == applicant_id
    ).all()
