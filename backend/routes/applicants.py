
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database import get_db
from backend.models.applicant import Applicant
from backend.schemas.applicant import (
    ApplicantCreate,
    ApplicantResponse
)

router = APIRouter(
    prefix="/api/applicants",
    tags=["Applicants"]
)


@router.post("/", response_model=ApplicantResponse, status_code=201)
def create_applicant(
    applicant_data: ApplicantCreate,
    db: Session = Depends(get_db)
):
    applicant = Applicant(**applicant_data.model_dump())

    try:
        db.add(applicant)
        db.commit()
        db.refresh(applicant)
        return applicant

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Applicant ID already exists"
        )


@router.get("/", response_model=list[ApplicantResponse])
def get_applicants(db: Session = Depends(get_db)):
    return db.query(Applicant).order_by(
        Applicant.created_at.desc()
    ).limit(100).all()


@router.get("/{applicant_id}", response_model=ApplicantResponse)
def get_applicant(
    applicant_id: str,
    db: Session = Depends(get_db)
):
    applicant = db.query(Applicant).filter(
        Applicant.applicant_id == applicant_id
    ).first()

    if not applicant:
        raise HTTPException(
            status_code=404,
            detail="Applicant not found"
        )

    return applicant
