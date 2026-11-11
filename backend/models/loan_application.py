
from sqlalchemy import Column, String, Numeric, Integer, DateTime, ForeignKey, func
from backend.database import Base


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    application_id = Column(String(30), primary_key=True)
    applicant_id = Column(
        String(30),
        ForeignKey("applicants.applicant_id"),
        nullable=False
    )
    product_id = Column(
        String(30),
        ForeignKey("loan_products.product_id"),
        nullable=False
    )
    requested_amount = Column(Numeric(14, 2), nullable=False)
    requested_term_months = Column(Integer, nullable=False)
    application_status = Column(String(40), default="SUBMITTED")
    submitted_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )
