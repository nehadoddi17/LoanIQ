
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database import get_db
from backend.models.applicant import Applicant
from backend.models.employment import Employment
from backend.schemas.employment import EmploymentCreate, EmploymentResponse

router = APIRouter(prefix="/api/employment", tags=["Employment"])


@router.post("/", response_model=EmploymentResponse, status_code=201)
def create_employment(data: EmploymentCreate, db: Session = Depends(get_db)):
    if not db.query(Applicant).filter(
        Applicant.applicant_id == data.applicant_id
    ).first():
        raise HTTPException(404, "Applicant not found")

    record = Employment(**data.model_dump())
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Employment ID already exists")


@router.get("/{applicant_id}", response_model=list[EmploymentResponse])
def get_employment(applicant_id: str, db: Session = Depends(get_db)):
    if not db.query(Applicant).filter(
        Applicant.applicant_id == applicant_id
    ).first():
        raise HTTPException(404, "Applicant not found")

    return db.query(Employment).filter(
        Employment.applicant_id == applicant_id
    ).all()
