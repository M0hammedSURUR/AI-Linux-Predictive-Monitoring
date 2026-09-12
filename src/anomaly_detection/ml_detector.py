from sklearn.ensemble import IsolationForest

from src.preprocessing.telemetry_preprocessor import ProcessedTelemetry


class MLAnomalyDetector:
    """Detect unusual telemetry patterns using Isolation Forest."""

    FEATURE_NAMES = [
        "cpu_percent",
        "memory_percent",
        "disk_percent",
        "load_1m",
    ]

    def __init__(
        self,
        contamination: float = 0.23,
        random_state: int = 42,
    ):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
        )

    def fit(
        self,
        records: list[ProcessedTelemetry],
    ) -> None:
        """Train the ML detector using telemetry records."""

        if len(records) < 10:
            raise ValueError(
                "At least 10 telemetry records are required "
                "to train the ML anomaly detector."
            )

        features = self._extract_features(records)

        self.model.fit(features)

    def predict(
        self,
        records: list[ProcessedTelemetry],
    ) -> list[bool]:
        """Return anomaly predictions for telemetry records."""

        if not records:
            return []

        features = self._extract_features(records)

        predictions = self.model.predict(features)

        return [
            prediction == -1
            for prediction in predictions
        ]

    def _extract_features(
        self,
        records: list[ProcessedTelemetry],
    ):
        """Extract the features used by the ML model."""

        return [
            [
                record.cpu_percent,
                record.memory_percent,
                record.disk_percent,
                record.load_1m,
            ]
            for record in records
        ]
