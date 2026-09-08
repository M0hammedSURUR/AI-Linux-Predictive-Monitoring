from dataclasses import dataclass
from datetime import datetime


@dataclass
class HealingAction:
    """Represents a proposed self-healing action awaiting approval."""

    timestamp: datetime
    metric: str
    action: str
    reason: str
    status: str
