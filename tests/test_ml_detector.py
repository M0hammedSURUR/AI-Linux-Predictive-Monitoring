from datetime import datetime, timezone

from src.anomaly_detection.ml_detector import MLAnomalyDetector
from src.preprocessing.telemetry_preprocessor import ProcessedTelemetry


def create_record(
    cpu: float,
    memory: float,
    disk: float,
    load: float,
) -> ProcessedTelemetry:
    """Create a test telemetry record."""

    return ProcessedTelemetry(
        timestamp=datetime.now(timezone.utc),
        cpu_percent=cpu,
        memory_percent=memory,
        swap_percent=0.0,
        disk_percent=disk,
        load_1m=load,
        process_count=100,
        disk_read_rate=0.0,
        disk_write_rate=0.0,
        network_send_rate=0.0,
        network_receive_rate=0.0,
        top_cpu_process=None,
        top_memory_process=None,
    )


def test_ml_detector_detects_anomalous_pattern():
    """Verify that Isolation Forest detects an unusual telemetry pattern."""

    normal_records = [
        create_record(10.0, 30.0, 15.0, 0.5),
        create_record(12.0, 31.0, 16.0, 0.6),
        create_record(11.0, 29.0, 14.0, 0.4),
        create_record(13.0, 30.0, 17.0, 0.7),
        create_record(10.0, 32.0, 15.0, 0.5),
        create_record(12.0, 31.0, 16.0, 0.6),
        create_record(11.0, 30.0, 15.0, 0.5),
        create_record(13.0, 29.0, 17.0, 0.7),
        create_record(10.0, 31.0, 14.0, 0.4),
        create_record(12.0, 30.0, 16.0, 0.6),
    ]

    anomaly_record = create_record(
        99.0,
        95.0,
        98.0,
        12.0,
    )

    records = normal_records + [anomaly_record]

    detector = MLAnomalyDetector(
        contamination=0.09,
        random_state=42,
    )

    detector.fit(normal_records)

    predictions = detector.predict(records)

    assert len(predictions) == len(records)
    assert bool(predictions[-1]) is True
