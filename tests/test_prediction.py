from datetime import datetime, timezone

from src.preprocessing.telemetry_preprocessor import ProcessedTelemetry
from src.prediction.predictor import TelemetryPredictor


def create_record(
    timestamp: datetime,
    cpu_percent: float = 20.0,
    memory_percent: float = 40.0,
    disk_percent: float = 50.0,
) -> ProcessedTelemetry:
    """Create a sample processed telemetry record for testing."""

    return ProcessedTelemetry(
        timestamp=timestamp,
        cpu_percent=cpu_percent,
        memory_percent=memory_percent,
        swap_percent=0.0,
        disk_percent=disk_percent,
        load_1m=0.5,
        process_count=100,
        disk_read_rate=100.0,
        disk_write_rate=100.0,
        network_send_rate=100.0,
        network_receive_rate=100.0,
        top_cpu_process="test_cpu",
        top_memory_process="test_memory",
    )


def test_predictor_requires_two_records():
    """Verify that prediction needs at least two records."""

    predictor = TelemetryPredictor()

    timestamp = datetime.now(timezone.utc)

    record = create_record(timestamp)

    predictions = predictor.predict([record])

    assert predictions == []


def test_cpu_prediction_is_generated():
    """Verify that CPU prediction is generated from a trend."""

    predictor = TelemetryPredictor()

    first_timestamp = datetime.now(timezone.utc)
    second_timestamp = first_timestamp.replace(
        microsecond=first_timestamp.microsecond + 1
    )

    first_record = create_record(
        first_timestamp,
        cpu_percent=20.0,
    )

    second_record = create_record(
        second_timestamp,
        cpu_percent=30.0,
    )

    predictions = predictor.predict(
        [first_record, second_record]
    )

    cpu_prediction = next(
        prediction
        for prediction in predictions
        if prediction.metric == "cpu_percent"
    )

    assert cpu_prediction.current_value == 30.0
    assert cpu_prediction.predicted_value == 40.0
    assert cpu_prediction.threshold == 80.0
    assert cpu_prediction.risk_level == "low"


def test_high_cpu_prediction_is_detected():
    """Verify that a predicted threshold violation is marked high risk."""

    predictor = TelemetryPredictor()

    first_timestamp = datetime.now(timezone.utc)
    second_timestamp = first_timestamp.replace(
        microsecond=first_timestamp.microsecond + 1
    )

    first_record = create_record(
        first_timestamp,
        cpu_percent=75.0,
    )

    second_record = create_record(
        second_timestamp,
        cpu_percent=85.0,
    )

    predictions = predictor.predict(
        [first_record, second_record]
    )

    cpu_prediction = next(
        prediction
        for prediction in predictions
        if prediction.metric == "cpu_percent"
    )

    assert cpu_prediction.predicted_value == 95.0
    assert cpu_prediction.risk_level == "high"
