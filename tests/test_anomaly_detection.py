from datetime import datetime, timezone

from src.anomaly_detection.detector import AnomalyDetector
from src.collector.models import TelemetryRecord


def create_record(
    cpu=20.0,
    memory=40.0,
    disk=50.0,
    load=1.0,
):
    """Create a telemetry record for testing."""

    return TelemetryRecord(
        timestamp=datetime.now(timezone.utc),
        cpu_percent=cpu,
        memory_percent=memory,
        swap_percent=0.0,
        disk_percent=disk,
        load_1m=load,
        disk_read_bytes=1000,
        disk_write_bytes=2000,
        network_bytes_sent=3000,
        network_bytes_received=4000,
        process_count=100,
        top_cpu_process="test_cpu_process",
        top_memory_process="test_memory_process",
    )


def test_normal_record_has_no_anomalies():
    detector = AnomalyDetector()

    record = create_record()

    results = detector.detect(record)

    assert results == []


def test_high_cpu_is_detected():
    detector = AnomalyDetector()

    record = create_record(cpu=95.0)

    results = detector.detect(record)

    assert len(results) == 1

    result = results[0]

    assert result.is_anomaly is True
    assert result.metric == "cpu_percent"
    assert result.observed_value == 95.0
    assert result.threshold == 80.0
    assert result.severity == "high"
    assert result.explanation == (
        "CPU usage is above the configured threshold."
    )


def test_multiple_anomalies_are_detected():
    detector = AnomalyDetector()

    record = create_record(
        cpu=95.0,
        memory=95.0,
        disk=95.0,
        load=10.0,
    )

    results = detector.detect(record)

    assert len(results) == 4

    metrics = {result.metric for result in results}

    assert metrics == {
        "cpu_percent",
        "memory_percent",
        "disk_percent",
        "load_1m",
    }


def test_critical_severity_is_detected():
    detector = AnomalyDetector()

    record = create_record(cpu=100.0)

    results = detector.detect(record)

    assert results[0].severity == "critical"


def test_medium_severity_is_detected():
    detector = AnomalyDetector()

    record = create_record(cpu=85.0)

    results = detector.detect(record)

    assert results[0].severity == "medium"
