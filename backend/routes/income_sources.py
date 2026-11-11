
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database import get_db
from backend.models.applicant import Applicant
from backend.models.income_source import IncomeSource
from backend.schemas.income_source import IncomeSourceCreate, IncomeSourceResponse

router = APIRouter(prefix="/api/income-sources", tags=["Income Sources"])


@router.post("/", response_model=IncomeSourceResponse, status_code=201)
def create_income(data: IncomeSourceCreate, db: Session = Depends(get_db)):
    if not db.query(Applicant).filter(
        Applicant.applicant_id == data.applicant_id
    ).first():
        raise HTTPException(404, "Applicant not found")

    record = IncomeSource(**data.model_dump())
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Income source ID already exists")


@router.get("/{applicant_id}", response_model=list[IncomeSourceResponse])
def get_income_sources(applicant_id: str, db: Session = Depends(get_db)):
    if not db.query(Applicant).filter(
        Applicant.applicant_id == applicant_id
    ).first():
        raise HTTPException(404, "Applicant not found")

    return db.query(IncomeSource).filter(
        IncomeSource.applicant_id == applicant_id
    ).all()
