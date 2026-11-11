
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services.anomaly_evaluation import evaluate_detection_results
from backend.models.ground_truth_anomaly import GroundTruthAnomaly

router = APIRouter(
    prefix="/api/anomaly-evaluation",
    tags=["Anomaly Evaluation"]
)


@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    count = db.query(GroundTruthAnomaly).count()

    if count == 0:
        raise HTTPException(
            409,
            "No ground-truth cases have been loaded yet"
        )

    return evaluate_detection_results(db)
