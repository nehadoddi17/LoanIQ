
from sqlalchemy.orm import Session

from backend.models.anomaly_case import AnomalyCase
from backend.models.ground_truth_anomaly import GroundTruthAnomaly


def evaluate_detection_results(db: Session):
    """
    Evaluate anomaly detection against all ground-truth
    application/anomaly-type combinations.

    Ground truth is independent of detector output.
    """

    ground_truth_rows = db.query(GroundTruthAnomaly).all()

    detected_rows = db.query(AnomalyCase).filter(
        AnomalyCase.detected == True
    ).all()

    # Each detected finding is identified by application and anomaly type.
    detected_pairs = {
        (row.application_id, row.anomaly_type)
        for row in detected_rows
    }

    tp = 0
    fp = 0
    fn = 0
    tn = 0

    for truth in ground_truth_rows:
        key = (
            truth.application_id,
            truth.expected_anomaly_type
        )

        actual = bool(truth.expected_anomaly)
        predicted = key in detected_pairs

        if actual and predicted:
            tp += 1
        elif not actual and predicted:
            fp += 1
        elif actual and not predicted:
            fn += 1
        else:
            tn += 1

    total = tp + fp + fn + tn

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    accuracy = (tp + tn) / total if total else 0.0

    return {
        "ground_truth_cases": len(ground_truth_rows),
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "accuracy": round(accuracy, 4)
    }
