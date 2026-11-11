
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.anomaly_case import AnomalyCase
from backend.services.anomaly_detection import run_anomaly_detection
from backend.schemas.anomaly import AnomalyResponse, AnomalyScanResponse


router = APIRouter(
    prefix="/api/anomalies",
    tags=["Anomaly Detection"]
)


@router.post("/scan", response_model=AnomalyScanResponse)
def scan_anomalies(db: Session = Depends(get_db)):
    return run_anomaly_detection(db)


@router.get("/", response_model=list[AnomalyResponse])
def get_anomalies(
    detected_only: bool = Query(default=True),
    anomaly_type: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(AnomalyCase)

    if detected_only:
        query = query.filter(AnomalyCase.detected.is_(True))

    if anomaly_type:
        query = query.filter(AnomalyCase.anomaly_type == anomaly_type)

    return query.order_by(AnomalyCase.detected_at.desc()).all()


@router.get(
    "/{application_id}",
    response_model=list[AnomalyResponse]
)
def get_application_anomalies(
    application_id: str,
    db: Session = Depends(get_db)
):
    return db.query(AnomalyCase).filter(
        AnomalyCase.application_id == application_id,
        AnomalyCase.detected.is_(True)
    ).order_by(AnomalyCase.detected_at.desc()).all()
