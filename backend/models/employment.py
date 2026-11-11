
from sqlalchemy import Column, String, Date, DateTime, Numeric, ForeignKey, func
from backend.database import Base


class Employment(Base):
    __tablename__ = "employment"

    employment_id = Column(String(30), primary_key=True)
    applicant_id = Column(
        String(30),
        ForeignKey("applicants.applicant_id"),
        nullable=False
    )
    employer_name = Column(String(200))
    employment_type = Column(String(50))
    job_title = Column(String(100))
    employment_start_date = Column(Date)
    annual_salary = Column(Numeric(14, 2))
    employment_status = Column(String(30))
    created_at = Column(DateTime, server_default=func.current_timestamp())
