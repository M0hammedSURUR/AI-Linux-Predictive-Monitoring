from datetime import datetime, timezone

from src.preprocessing.telemetry_preprocessor import ProcessedTelemetry
from src.prediction.models import PredictionResult


class TelemetryPredictor:
    """
    Performs simple trend-based prediction on processed telemetry.

    This is the first prediction layer of the project.
    It uses recent telemetry values and estimates the next value
    using a simple linear trend.
    """

    # NEW: Prediction thresholds
    CPU_THRESHOLD = 80.0
    MEMORY_THRESHOLD = 80.0
    DISK_THRESHOLD = 90.0

    def predict(
        self,
        records: list[ProcessedTelemetry],
    ) -> list[PredictionResult]:
        """Generate predictions from processed telemetry records."""

        if len(records) < 2:
            return []

        predictions: list[PredictionResult] = []

        latest = records[-1]
        previous = records[-2]

        # NEW: Predict CPU usage
        predictions.append(
            self._create_prediction(
                timestamp=latest.timestamp,
                metric="cpu_percent",
                current_value=latest.cpu_percent,
                previous_value=previous.cpu_percent,
                threshold=self.CPU_THRESHOLD,
            )
        )

        # NEW: Predict memory usage
        predictions.append(
            self._create_prediction(
                timestamp=latest.timestamp,
                metric="memory_percent",
                current_value=latest.memory_percent,
                previous_value=previous.memory_percent,
                threshold=self.MEMORY_THRESHOLD,
            )
        )

        # NEW: Predict disk usage
        predictions.append(
            self._create_prediction(
                timestamp=latest.timestamp,
                metric="disk_percent",
                current_value=latest.disk_percent,
                previous_value=previous.disk_percent,
                threshold=self.DISK_THRESHOLD,
            )
        )

        return predictions

    def _create_prediction(
        self,
        timestamp: datetime,
        metric: str,
        current_value: float,
        previous_value: float,
        threshold: float,
    ) -> PredictionResult:
        """Create one prediction using the latest telemetry trend."""

        # NEW: Calculate the change between the latest two observations
        change = current_value - previous_value

        # NEW: Estimate the next value
        predicted_value = max(0.0, current_value + change)

        # NEW: Determine prediction risk
        if predicted_value >= threshold:
            risk_level = "high"
        elif predicted_value >= threshold * 0.8:
            risk_level = "medium"
        else:
            risk_level = "low"

        # NEW: Generate a human-readable message
        if predicted_value >= threshold:
            message = (
                f"{metric} is predicted to reach "
                f"{predicted_value:.1f}%, exceeding the threshold "
                f"of {threshold:.1f}%."
            )
        elif change > 0:
            message = (
                f"{metric} is increasing. "
                f"Predicted next value: {predicted_value:.1f}%."
            )
        else:
            message = (
                f"{metric} is stable or decreasing. "
                f"Predicted next value: {predicted_value:.1f}%."
            )

        return PredictionResult(
            timestamp=timestamp,
            metric=metric,
            current_value=current_value,
            predicted_value=predicted_value,
            threshold=threshold,
            risk_level=risk_level,
            message=message,
        )
