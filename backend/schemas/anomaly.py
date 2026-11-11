
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AnomalyResponse(BaseModel):
    anomaly_id: str
    application_id: str | None = None
    anomaly_type: str
    description: str | None = None
    detected: bool
    detected_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class AnomalyScanResponse(BaseModel):
    applications_scanned: int
    anomalies_detected: int
    findings: list[dict]
