
from sqlalchemy import (
    Column, String, Numeric, DateTime,
    ForeignKey, func
)
from backend.database import Base


class AffordabilityCheck(Base):
    __tablename__ = "affordability_checks"

    check_id = Column(String(30), primary_key=True)

    application_id = Column(
        String(30),
        ForeignKey("loan_applications.application_id"),
        nullable=False
    )

    monthly_income = Column(Numeric(14, 2))
    monthly_existing_obligations = Column(Numeric(14, 2))
    proposed_emi = Column(Numeric(14, 2))
    debt_to_income_ratio = Column(Numeric(8, 4))
    disposable_income = Column(Numeric(14, 2))
    check_status = Column(String(30))

    checked_at = Column(
        DateTime,
        server_default=func.current_timestamp()
    )
