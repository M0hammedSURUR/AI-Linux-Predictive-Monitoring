from src.anomaly_detection.models import AnomalyResult
from src.preprocessing.telemetry_preprocessor import ProcessedTelemetry


class AnomalyDetector:
    """Detect abnormal system conditions using threshold rules."""

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

    def detect(
        self,
        record: ProcessedTelemetry,
    ) -> list[AnomalyResult]:
        """Check one processed telemetry record for anomalies."""

        anomalies = []

        checks = [
            (
                "cpu_percent",
                record.cpu_percent,
                self.cpu_threshold,
                "CPU usage is above the configured threshold.",
            ),
            (
                "memory_percent",
                record.memory_percent,
                self.memory_threshold,
                "Memory usage is above the configured threshold.",
            ),
            (
                "disk_percent",
                record.disk_percent,
                self.disk_threshold,
                "Disk usage is above the configured threshold.",
            ),
            (
                "load_1m",
                record.load_1m,
                self.load_threshold,
                "System load is above the configured threshold.",
            ),
        ]

        for metric, observed_value, threshold, explanation in checks:
            if observed_value >= threshold:
                anomalies.append(
                    AnomalyResult(
                        timestamp=record.timestamp,
                        is_anomaly=True,
                        metric=metric,
                        observed_value=observed_value,
                        threshold=threshold,
                        severity=self._calculate_severity(
                            observed_value,
                            threshold,
                        ),
                        explanation=explanation,
                    )
                )

        return anomalies

    def _calculate_severity(
        self,
        observed_value: float,
        threshold: float,
    ) -> str:
        """Calculate anomaly severity from threshold exceedance."""

        if observed_value >= threshold * 1.25:
            return "critical"

        if observed_value >= threshold * 1.10:
            return "high"

        return "medium"
