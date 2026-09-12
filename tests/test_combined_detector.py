from datetime import datetime, timezone

from src.anomaly_detection.combined_detector import CombinedAnomalyDetector
from src.anomaly_detection.models import AnomalyResult
from src.preprocessing.telemetry_preprocessor import ProcessedTelemetry


def create_record() -> ProcessedTelemetry:
    """Create a sample processed telemetry record."""

    return ProcessedTelemetry(
        timestamp=datetime.now(timezone.utc),
        cpu_percent=25.0,
        memory_percent=40.0,
        swap_percent=0.0,
        disk_percent=15.0,
        load_1m=0.5,
        process_count=100,
        disk_read_rate=0.0,
        disk_write_rate=0.0,
        network_send_rate=0.0,
        network_receive_rate=0.0,
        top_cpu_process="python",
        top_memory_process="python",
    )


def create_rule_anomaly() -> AnomalyResult:
    """Create a sample rule-based anomaly."""

    record = create_record()

    return AnomalyResult(
        timestamp=record.timestamp,
        is_anomaly=True,
        metric="cpu_percent",
        observed_value=95.0,
        threshold=80.0,
        severity="high",
        explanation="CPU usage is above the configured threshold.",
    )


def test_combined_detector_rule_and_ml_agreement():
    """Both detectors identifying an anomaly should produce high confidence."""

    detector = CombinedAnomalyDetector()
    record = create_record()
    rule_anomalies = [create_rule_anomaly()]

    result = detector.analyze(
        telemetry=record,
        rule_anomalies=rule_anomalies,
        ml_is_anomaly=True,
    )

    assert result.ml_is_anomaly is True
    assert result.confidence == "high"
    assert "Both rule-based and ML detection" in result.explanation


def test_combined_detector_rule_only():
    """A rule anomaly without ML support should produce medium confidence."""

    detector = CombinedAnomalyDetector()
    record = create_record()
    rule_anomalies = [create_rule_anomaly()]

    result = detector.analyze(
        telemetry=record,
        rule_anomalies=rule_anomalies,
        ml_is_anomaly=False,
    )

    assert result.confidence == "medium"
    assert result.ml_is_anomaly is False


def test_combined_detector_ml_only():
    """An ML-only anomaly should remain experimental."""

    detector = CombinedAnomalyDetector()
    record = create_record()

    result = detector.analyze(
        telemetry=record,
        rule_anomalies=[],
        ml_is_anomaly=True,
    )

    assert result.confidence == "experimental"
    assert result.ml_is_anomaly is True


def test_combined_detector_normal():
    """No anomaly from either detector should produce normal status."""

    detector = CombinedAnomalyDetector()
    record = create_record()

    result = detector.analyze(
        telemetry=record,
        rule_anomalies=[],
        ml_is_anomaly=False,
    )

    assert result.confidence == "normal"
    assert result.ml_is_anomaly is False
