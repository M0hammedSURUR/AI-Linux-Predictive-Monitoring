from datetime import datetime

from src.preprocessing.telemetry_preprocessor import ProcessedTelemetry
from src.prediction.models import PredictionResult


class TelemetryPredictor:
    """
    Predict future resource usage from recent telemetry history.

    The predictor uses a rolling linear trend over recent observations
    instead of relying only on the last two values.
    """

    CPU_THRESHOLD = 80.0
    MEMORY_THRESHOLD = 80.0
    DISK_THRESHOLD = 90.0

    HISTORY_SIZE = 5

    def predict(
        self,
        records: list[ProcessedTelemetry],
    ) -> list[PredictionResult]:
        """Generate predictions from recent processed telemetry."""

        if len(records) < 2:
            return []

        recent_records = records[-self.HISTORY_SIZE:]

        latest = recent_records[-1]

        predictions: list[PredictionResult] = []

        predictions.append(
            self._create_prediction(
                timestamp=latest.timestamp,
                metric="cpu_percent",
                current_value=latest.cpu_percent,
                values=[
                    record.cpu_percent
                    for record in recent_records
                ],
                threshold=self.CPU_THRESHOLD,
            )
        )

        predictions.append(
            self._create_prediction(
                timestamp=latest.timestamp,
                metric="memory_percent",
                current_value=latest.memory_percent,
                values=[
                    record.memory_percent
                    for record in recent_records
                ],
                threshold=self.MEMORY_THRESHOLD,
            )
        )

        predictions.append(
            self._create_prediction(
                timestamp=latest.timestamp,
                metric="disk_percent",
                current_value=latest.disk_percent,
                values=[
                    record.disk_percent
                    for record in recent_records
                ],
                threshold=self.DISK_THRESHOLD,
            )
        )

        return predictions

    def _create_prediction(
        self,
        timestamp: datetime,
        metric: str,
        current_value: float,
        values: list[float],
        threshold: float,
    ) -> PredictionResult:
        """Create one prediction using a linear trend."""

        if len(values) < 2:
            predicted_value = current_value
        else:
            x_values = list(range(len(values)))
            x_mean = sum(x_values) / len(x_values)
            y_mean = sum(values) / len(values)

            numerator = sum(
                (x - x_mean) * (y - y_mean)
                for x, y in zip(x_values, values)
            )

            denominator = sum(
                (x - x_mean) ** 2
                for x in x_values
            )

            slope = numerator / denominator

            predicted_value = current_value + slope

        predicted_value = max(0.0, predicted_value)

        if predicted_value >= threshold:
            risk_level = "high"
        elif predicted_value >= threshold * 0.8:
            risk_level = "medium"
        else:
            risk_level = "low"

        if predicted_value >= threshold:
            message = (
                f"{metric} is predicted to reach "
                f"{predicted_value:.1f}%, exceeding the threshold "
                f"of {threshold:.1f}%."
            )
        elif predicted_value > current_value:
            message = (
                f"{metric} is increasing based on the recent trend. "
                f"Predicted next value: {predicted_value:.1f}%."
            )
        else:
            message = (
                f"{metric} is stable or decreasing based on the "
                f"recent trend. Predicted next value: "
                f"{predicted_value:.1f}%."
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
