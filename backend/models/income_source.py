
from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey, func
from backend.database import Base


class IncomeSource(Base):
    __tablename__ = "income_sources"

    income_source_id = Column(String(30), primary_key=True)
    applicant_id = Column(
        String(30),
        ForeignKey("applicants.applicant_id"),
        nullable=False
    )
    source_type = Column(String(50))
    source_name = Column(String(200))
    monthly_amount = Column(Numeric(14, 2))
    verification_status = Column(String(30))
    reported_at = Column(DateTime, server_default=func.current_timestamp())
