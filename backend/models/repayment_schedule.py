
from sqlalchemy import (
    Column, String, Numeric, Integer, DateTime,
    ForeignKey, func
)
from backend.database import Base


class RepaymentSchedule(Base):
    __tablename__ = "repayment_schedules"

    schedule_id = Column(String(30), primary_key=True)

    application_id = Column(
        String(30),
        ForeignKey("loan_applications.application_id"),
        nullable=False
    )

    principal_amount = Column(Numeric(14, 2), nullable=False)
    total_interest = Column(Numeric(14, 2))
    total_payable = Column(Numeric(14, 2))
    expected_installment_count = Column(Integer)
    calculated_installment_total = Column(Numeric(14, 2))
    reconciliation_status = Column(String(30))

    generated_at = Column(
        DateTime,
        server_default=func.current_timestamp()
    )
