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
from datetime import datetime, timezone

import psutil

from .models import TelemetryRecord


class SystemCollector:
    """Collect system-level Linux telemetry."""

    def collect(self) -> TelemetryRecord:
        """Collect one telemetry snapshot."""

        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disk = psutil.disk_usage("/")

        disk_io = psutil.disk_io_counters()
        network_io = psutil.net_io_counters()

        processes = list(psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]))

        process_count = len(processes)

        top_cpu_process = self._top_process(processes, "cpu_percent")
        top_memory_process = self._top_process(processes, "memory_percent")

        load_1m = psutil.getloadavg()[0]

        return TelemetryRecord(
            timestamp=datetime.now(timezone.utc),
            cpu_percent=psutil.cpu_percent(interval=0.1),
            memory_percent=memory.percent,
            swap_percent=swap.percent,
            disk_percent=disk.percent,
            load_1m=load_1m,
            disk_read_bytes=disk_io.read_bytes if disk_io else 0,
            disk_write_bytes=disk_io.write_bytes if disk_io else 0,
            network_bytes_sent=network_io.bytes_sent if network_io else 0,
            network_bytes_received=network_io.bytes_recv if network_io else 0,
            process_count=process_count,
            top_cpu_process=top_cpu_process,
            top_memory_process=top_memory_process,
        )

    @staticmethod
    def _top_process(processes, metric: str) -> str:
        """Return the name of the process with the highest metric."""

        valid_processes = []

        for process in processes:
            try:
                value = process.info.get(metric)

                if value is not None:
                    valid_processes.append((value, process.info.get("name") or "unknown"))

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if not valid_processes:
            return "unknown"

        return max(valid_processes, key=lambda item: item[0])[1]
