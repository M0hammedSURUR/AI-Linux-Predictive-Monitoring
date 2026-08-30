from dataclasses import dataclass
from datetime import datetime


@dataclass
class PredictionResult:
    """Represents a prediction generated from processed telemetry."""

    timestamp: datetime
    metric: str
    current_value: float
    predicted_value: float
    threshold: float
    risk_level: str
    message: str
