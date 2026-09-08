from dataclasses import dataclass
from datetime import datetime


@dataclass
class HealingAuditLog:
    """Records the result of a self-healing action."""

    timestamp: datetime
    metric: str
    action: str
    approval_status: str
    execution_status: str
    result: str
    error: str | None = None
