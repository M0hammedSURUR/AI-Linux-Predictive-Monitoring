from dataclasses import dataclass
from datetime import datetime


@dataclass
class AnomalyResult:
    """Represents the result of anomaly detection for one telemetry observation."""

    timestamp: datetime
    is_anomaly: bool
    metric: str | None
    observed_value: float | None
    threshold: float | None
    severity: str
    explanation: str
