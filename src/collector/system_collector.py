from datetime import datetime, timezone

import psutil

from .models import TelemetryRecord


class SystemCollector:
    """Collect basic Linux system telemetry."""

    def collect(self) -> TelemetryRecord:
        """Collect one telemetry snapshot."""

        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disk = psutil.disk_usage("/")

        load_1m = psutil.getloadavg()[0]

        return TelemetryRecord(
            timestamp=datetime.now(timezone.utc),
            cpu_percent=psutil.cpu_percent(interval=0.1),
            memory_percent=memory.percent,
            swap_percent=swap.percent,
            disk_percent=disk.percent,
            load_1m=load_1m,
        )
