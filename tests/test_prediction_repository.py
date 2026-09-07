from datetime import datetime, timezone

from src.database.database import (
    CREATE_PREDICTION_EVENTS_TABLE,
    CREATE_PREDICTION_TIMESTAMP_INDEX,
)
from src.prediction.models import PredictionResult
from src.prediction.repository import PredictionRepository


def create_prediction() -> PredictionResult:
    """Create a sample prediction for testing."""

    return PredictionResult(
        timestamp=datetime.now(timezone.utc),
        metric="cpu_percent",
        current_value=75.0,
        predicted_value=85.0,
        threshold=80.0,
        risk_level="high",
        message="CPU usage is predicted to exceed the threshold.",
    )


def test_prediction_can_be_saved(tmp_path):
    """Verify that a prediction can be stored and retrieved."""

    # NEW: Use a temporary database for the test
    database_path = tmp_path / "test_monitoring.db"

    # NEW: Initialize the prediction table in the test database
    import sqlite3

    with sqlite3.connect(database_path) as connection:
        connection.execute(CREATE_PREDICTION_EVENTS_TABLE)
        connection.execute(CREATE_PREDICTION_TIMESTAMP_INDEX)
        connection.commit()

    # Create the prediction repository
    repository = PredictionRepository(database_path)

    prediction = create_prediction()

    # Save the prediction
    repository.save(prediction)

    # Retrieve saved predictions
    predictions = repository.get_all()

    assert len(predictions) == 1

    saved_prediction = predictions[0]

    assert saved_prediction.metric == "cpu_percent"
    assert saved_prediction.current_value == 75.0
    assert saved_prediction.predicted_value == 85.0
    assert saved_prediction.threshold == 80.0
    assert saved_prediction.risk_level == "high"
