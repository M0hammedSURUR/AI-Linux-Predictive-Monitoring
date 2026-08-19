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
        timestamp=__import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ),
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


def test_normal_record_is_not_an_anomaly():
    detector = AnomalyDetector()

    record = create_record()

    result = detector.detect(record)

    assert result.is_anomaly is False
    assert result.reasons == []


def test_high_cpu_is_detected():
    detector = AnomalyDetector()

    record = create_record(cpu=95.0)

    result = detector.detect(record)

    assert result.is_anomaly is True
    assert "High CPU usage" in result.reasons


def test_multiple_anomalies_are_detected():
    detector = AnomalyDetector()

    record = create_record(
        cpu=95.0,
        memory=95.0,
        disk=95.0,
        load=10.0,
    )

    result = detector.detect(record)

    assert result.is_anomaly is True
    assert "High CPU usage" in result.reasons
    assert "High memory usage" in result.reasons
    assert "High disk usage" in result.reasons
    assert "High system load" in result.reasons
