
from sqlalchemy import (
    Column, String, Integer, Date, Numeric, ForeignKey
)
from backend.database import Base


class RepaymentInstallment(Base):
    __tablename__ = "repayment_installments"

    installment_id = Column(String(30), primary_key=True)

    schedule_id = Column(
        String(30),
        ForeignKey("repayment_schedules.schedule_id"),
        nullable=False
    )

    installment_number = Column(Integer, nullable=False)
    due_date = Column(Date, nullable=False)
    principal_component = Column(Numeric(14, 2))
    interest_component = Column(Numeric(14, 2))
    installment_amount = Column(Numeric(14, 2))
    payment_status = Column(String(30), default="PENDING")
