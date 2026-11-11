
from sqlalchemy import (
    Column, String, DateTime, ForeignKey, func
)
from backend.database import Base


class ApplicationDocument(Base):
    __tablename__ = "application_documents"

    document_id = Column(String(30), primary_key=True)
    application_id = Column(
        String(30),
        ForeignKey("loan_applications.application_id"),
        nullable=False
    )
    document_type = Column(String(80))
    file_name = Column(String(255))
    verification_status = Column(String(30), default="PENDING")
    uploaded_at = Column(DateTime, server_default=func.current_timestamp())
    verified_at = Column(DateTime)
