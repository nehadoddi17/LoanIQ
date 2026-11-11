
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, func
from backend.database import Base


class LoanDecision(Base):
    __tablename__ = "loan_decisions"

    decision_id = Column(String(30), primary_key=True)

    application_id = Column(
        String(30),
        ForeignKey("loan_applications.application_id"),
        nullable=False
    )

    decision = Column(String(30), nullable=False)
    reason = Column(Text)
    decided_by = Column(String(100))

    decision_at = Column(
        DateTime,
        server_default=func.current_timestamp()
    )
