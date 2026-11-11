
from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey, func
from backend.database import Base


class CreditFacility(Base):
    __tablename__ = "credit_facilities"

    facility_id = Column(String(30), primary_key=True)
    applicant_id = Column(
        String(30),
        ForeignKey("applicants.applicant_id"),
        nullable=False
    )
    lender_name = Column(String(200))
    facility_type = Column(String(50))
    outstanding_balance = Column(Numeric(14, 2))
    monthly_obligation = Column(Numeric(14, 2))
    facility_status = Column(String(30))
    reported_at = Column(DateTime, server_default=func.current_timestamp())
