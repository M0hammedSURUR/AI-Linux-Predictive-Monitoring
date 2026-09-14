from datetime import datetime, timedelta, timezone

from experiments.prediction.evaluate_prediction import (
    create_record,
    evaluate_metric,
)
from src.prediction.predictor import TelemetryPredictor


def test_prediction_evaluation_returns_valid_metrics():
    """Verify that prediction evaluation returns valid MAE and RMSE."""

    base_timestamp = datetime.now(timezone.utc)

    records = [
        create_record(
            timestamp=base_timestamp + timedelta(seconds=index),
            cpu_percent=cpu,
            memory_percent=memory,
            disk_percent=disk,
        )
        for index, (cpu, memory, disk) in enumerate(
            [
                (20.0, 40.0, 50.0),
                (23.0, 41.0, 51.0),
                (25.0, 43.0, 52.0),
                (29.0, 44.0, 53.0),
            ]
        )
    ]

    predictor = TelemetryPredictor()

    mae, rmse = evaluate_metric(
        predictor=predictor,
        records=records,
        metric="cpu_percent",
    )

    assert mae >= 0.0
    assert rmse >= 0.0
