from dataclasses import dataclass

from src.preprocessing.telemetry_preprocessor import ProcessedTelemetry


@dataclass
class AnomalyResult:
    """Represents anomaly detection results for one telemetry record."""

    timestamp: object
    is_anomaly: bool
    reasons: list[str]


class AnomalyDetector:
    """Detects abnormal system conditions using threshold rules."""

    def __init__(
        self,
        cpu_threshold: float = 80.0,
        memory_threshold: float = 80.0,
        disk_threshold: float = 90.0,
        load_threshold: float = 4.0,
    ):
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.disk_threshold = disk_threshold
        self.load_threshold = load_threshold

    def detect(self, record: ProcessedTelemetry) -> AnomalyResult:
        """Check one processed telemetry record for anomalies."""

        reasons = []

        if record.cpu_percent >= self.cpu_threshold:
            reasons.append("High CPU usage")

        if record.memory_percent >= self.memory_threshold:
            reasons.append("High memory usage")

        if record.disk_percent >= self.disk_threshold:
            reasons.append("High disk usage")

        if record.load_1m >= self.load_threshold:
            reasons.append("High system load")

        return AnomalyResult(
            timestamp=record.timestamp,
            is_anomaly=bool(reasons),
            reasons=reasons,
        )
