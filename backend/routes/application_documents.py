
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database import get_db
from backend.models.loan_application import LoanApplication
from backend.models.application_document import ApplicationDocument
from backend.schemas.application_document import (
    ApplicationDocumentCreate,
    ApplicationDocumentResponse
)

router = APIRouter(
    prefix="/api/documents",
    tags=["Application Documents"]
)


@router.post("/", response_model=ApplicationDocumentResponse, status_code=201)
def create_document(data: ApplicationDocumentCreate, db: Session = Depends(get_db)):
    if not db.query(LoanApplication).filter(
        LoanApplication.application_id == data.application_id
    ).first():
        raise HTTPException(404, "Loan application not found")

    record = ApplicationDocument(**data.model_dump())
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Document ID already exists")


@router.get("/{application_id}", response_model=list[ApplicationDocumentResponse])
def get_documents(application_id: str, db: Session = Depends(get_db)):
    if not db.query(LoanApplication).filter(
        LoanApplication.application_id == application_id
    ).first():
        raise HTTPException(404, "Loan application not found")

    return db.query(ApplicationDocument).filter(
        ApplicationDocument.application_id == application_id
    ).all()


@router.patch("/{document_id}/verify", response_model=ApplicationDocumentResponse)
def verify_document(document_id: str, db: Session = Depends(get_db)):
    record = db.query(ApplicationDocument).filter(
        ApplicationDocument.document_id == document_id
    ).first()

    if not record:
        raise HTTPException(404, "Document not found")

    if record.verification_status == "VERIFIED":
        raise HTTPException(409, "Document is already verified")

    record.verification_status = "VERIFIED"
    record.verified_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(record)
    return record
