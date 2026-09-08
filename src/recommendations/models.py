from dataclasses import dataclass
from datetime import datetime


@dataclass
class Recommendation:
    """Represents a recommended action for a system condition."""

    timestamp: datetime
    metric: str
    severity: str
    title: str
    description: str
    suggested_action: str
