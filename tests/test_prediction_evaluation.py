from datetime import datetime, timedelta, timezone

from experiments.prediction.evaluate_prediction import (
    create_record,
    evaluate_metric,
)
from src.prediction.predictor import TelemetryPredictor


def test_prediction_evaluation_returns_valid_metrics():
    """Verify that prediction evaluation produces valid MAE and RMSE values."""

    base_timestamp = datetime.now(timezone.utc)

    cpu_values = [
        20.0,
        23.0,
        24.0,
        28.0,
        27.0,
        32.0,
        34.0,
        35.0,
        39.0,
        40.0,
    ]

    memory_values = [
        40.0,
        41.5,
        42.0,
        44.0,
        43.5,
        46.0,
        47.5,
        48.0,
        50.0,
        51.0,
    ]

    disk_values = [
        50.0,
        50.8,
        51.2,
        52.5,
        52.0,
        53.5,
        54.2,
        55.0,
        55.8,
        57.0,
    ]

    records = []

    for index in range(10):
        records.append(
            create_record(
                timestamp=base_timestamp + timedelta(seconds=index),
                cpu_percent=cpu_values[index],
                memory_percent=memory_values[index],
                disk_percent=disk_values[index],
            )
        )

    predictor = TelemetryPredictor()

    for metric in [
        "cpu_percent",
        "memory_percent",
        "disk_percent",
    ]:
        mae, rmse = evaluate_metric(
            predictor=predictor,
            records=records,
            metric=metric,
        )

        assert mae >= 0.0
        assert rmse >= 0.0
        assert mae > 0.0
        assert rmse > 0.0
