
from sqlalchemy import (
    Column, String, Text, Boolean, DateTime, ForeignKey
)
from backend.database import Base


class AnomalyCase(Base):
    __tablename__ = "anomaly_cases"

    anomaly_id = Column(String(30), primary_key=True)

    application_id = Column(
        String(30),
        ForeignKey("loan_applications.application_id")
    )

    anomaly_type = Column(String(100), nullable=False)
    description = Column(Text)
    detected = Column(Boolean, default=False)
    detected_at = Column(DateTime)
