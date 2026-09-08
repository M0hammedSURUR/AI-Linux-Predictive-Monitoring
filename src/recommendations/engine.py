from src.anomaly_detection.models import AnomalyResult
from src.prediction.models import PredictionResult
from src.recommendations.models import Recommendation


class RecommendationEngine:
    """Generates safe, human-readable recommendations."""

    def generate_from_anomaly(
        self,
        anomaly: AnomalyResult,
    ) -> list[Recommendation]:
        """Generate a recommendation from an anomaly result."""

        # NEW: Do not recommend actions for normal conditions
        if not anomaly.is_anomaly:
            return []

        # NEW: CPU recommendation based on the actual anomaly metric
        if anomaly.metric == "cpu_percent":
            return [
                Recommendation(
                    timestamp=anomaly.timestamp,
                    metric="cpu_percent",
                    severity=anomaly.severity,
                    title="High CPU Usage",
                    description=(
                        "CPU usage is above the configured monitoring "
                        "threshold."
                    ),
                    suggested_action=(
                        "Check the top CPU-consuming process and "
                        "consider stopping or restarting it if appropriate."
                    ),
                )
            ]

        # NEW: Memory recommendation
        if anomaly.metric == "memory_percent":
            return [
                Recommendation(
                    timestamp=anomaly.timestamp,
                    metric="memory_percent",
                    severity=anomaly.severity,
                    title="High Memory Usage",
                    description=(
                        "Memory usage is above the configured monitoring "
                        "threshold."
                    ),
                    suggested_action=(
                        "Inspect memory-intensive processes and consider "
                        "closing or restarting unnecessary processes."
                    ),
                )
            ]

        # NEW: Disk recommendation
        if anomaly.metric == "disk_percent":
            return [
                Recommendation(
                    timestamp=anomaly.timestamp,
                    metric="disk_percent",
                    severity=anomaly.severity,
                    title="High Disk Usage",
                    description=(
                        "Disk usage is above the configured monitoring "
                        "threshold."
                    ),
                    suggested_action=(
                        "Check disk usage and identify large or unnecessary "
                        "files before taking cleanup actions."
                    ),
                )
            ]

        # NEW: Load recommendation
        if anomaly.metric == "load_1m":
            return [
                Recommendation(
                    timestamp=anomaly.timestamp,
                    metric="load_1m",
                    severity=anomaly.severity,
                    title="High System Load",
                    description=(
                        "The system load is above the configured "
                        "monitoring threshold."
                    ),
                    suggested_action=(
                        "Inspect active processes and determine which "
                        "workloads are contributing to the high system load."
                    ),
                )
            ]

        # NEW: Unknown metrics produce no recommendation
        return []

    def generate_from_prediction(
        self,
        prediction: PredictionResult,
    ) -> list[Recommendation]:
        """Generate a recommendation from a prediction result."""

        # Only high-risk predictions require a recommendation
        if prediction.risk_level != "high":
            return []

        return [
            Recommendation(
                timestamp=prediction.timestamp,
                metric=prediction.metric,
                severity="high",
                title=f"Predicted High {prediction.metric}",
                description=(
                    f"{prediction.metric} is predicted to reach "
                    f"{prediction.predicted_value:.1f}%."
                ),
                suggested_action=(
                    "Monitor the metric closely and investigate the "
                    "responsible process or resource before the threshold "
                    "is exceeded."
                ),
            )
        ]
