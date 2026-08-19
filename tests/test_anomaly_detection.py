from datetime import datetime, timezone

from src.anomaly_detection.detector import AnomalyDetector
from src.preprocessing.telemetry_preprocessor import ProcessedTelemetry


def create_record(
    cpu_percent=25.0,
    memory_percent=40.0,
    disk_percent=50.0,
    load_1m=1.5,
):
    return ProcessedTelemetry(
        timestamp=datetime.now(timezone.utc),
        cpu_percent=cpu_percent,
        memory_percent=memory_percent,
        swap_percent=0.0,
        disk_percent=disk_percent,
        load_1m=load_1m,
        process_count=100,
        disk_read_rate=1000.0,
        disk_write_rate=2000.0,
        network_send_rate=3000.0,
        network_receive_rate=4000.0,
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

    record = create_record(cpu_percent=95.0)

    result = detector.detect(record)

    assert result.is_anomaly is True
    assert "High CPU usage" in result.reasons


def test_multiple_anomalies_are_detected():
    detector = AnomalyDetector()

    record = create_record(
        cpu_percent=95.0,
        memory_percent=90.0,
        disk_percent=95.0,
        load_1m=5.0,
    )

    result = detector.detect(record)

    assert result.is_anomaly is True
    assert len(result.reasons) == 4
