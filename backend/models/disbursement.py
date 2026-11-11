
from sqlalchemy import (
    Column, String, Numeric, DateTime, ForeignKey, func
)
from backend.database import Base


class Disbursement(Base):
    __tablename__ = "disbursements"

    disbursement_id = Column(String(30), primary_key=True)

    application_id = Column(
        String(30),
        ForeignKey("loan_applications.application_id"),
        nullable=False
    )

    amount = Column(Numeric(14, 2), nullable=False)
    disbursement_status = Column(String(30))

    disbursed_at = Column(DateTime)
    transaction_reference = Column(String(100))
