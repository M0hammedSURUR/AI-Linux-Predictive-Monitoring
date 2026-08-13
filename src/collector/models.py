from dataclasses import dataclass
from datetime import datetime


@dataclass
class TelemetryRecord:
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    swap_percent: float
    disk_percent: float
    load_1m: float
