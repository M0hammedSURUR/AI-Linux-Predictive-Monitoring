from dataclasses import dataclass
from datetime import datetime


@dataclass
class TelemetryRecord:
    """Represents one system telemetry snapshot."""

    timestamp: datetime

    # CPU and memory
    cpu_percent: float
    memory_percent: float
    swap_percent: float

    # Disk and load
    disk_percent: float
    load_1m: float
    disk_read_bytes: int
    disk_write_bytes: int

    # Network
    network_bytes_sent: int
    network_bytes_received: int

    # Processes
    process_count: int
    top_cpu_process: str
    top_memory_process: str
