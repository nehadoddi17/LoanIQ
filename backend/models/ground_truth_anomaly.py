
from sqlalchemy import Column, String, Boolean, Text, ForeignKey
from backend.database import Base


class GroundTruthAnomaly(Base):
    __tablename__ = "ground_truth_anomalies"

    ground_truth_id = Column(String(30), primary_key=True)

    anomaly_id = Column(
        String(30),
        ForeignKey("anomaly_cases.anomaly_id"),
        nullable=True
    )

    application_id = Column(
        String(30),
        ForeignKey("loan_applications.application_id"),
        nullable=False
    )

    expected_anomaly = Column(Boolean, nullable=False)
    expected_anomaly_type = Column(String(100), nullable=False)
    notes = Column(Text)
