from dataclasses import dataclass
from datetime import datetime


@dataclass
class AnomalyEvent:
    """Represents one detected anomaly event."""

    timestamp: datetime

    # Indicates whether the telemetry record is anomalous.
    is_anomaly: bool

    # Severity assigned to the anomaly.
    severity: str

    # Human-readable reasons for the anomaly.
    reasons: list[str]

    # Time when the anomaly event was created.
    created_at: datetime
