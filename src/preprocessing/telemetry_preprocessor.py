from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.database.repository import TelemetryRepository


@dataclass
class ProcessedTelemetry:
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    swap_percent: float
    disk_percent: float
    load_1m: float
    process_count: int

    disk_read_rate: float
    disk_write_rate: float
    network_send_rate: float
    network_receive_rate: float

    top_cpu_process: str | None
    top_memory_process: str | None


class TelemetryPreprocessor:
    """Convert stored telemetry into analysis-ready features."""

    def __init__(self, repository: TelemetryRepository):
        self.repository = repository

    def process(self, limit: int | None = None) -> List[ProcessedTelemetry]:
        records = self.repository.get_recent_records(limit=limit)

        if not records:
            return []

        records = sorted(records, key=lambda record: record.timestamp)

        processed = []

        previous = None

        for record in records:
            if previous is None:
                previous = record
                continue

            elapsed = (
                record.timestamp - previous.timestamp
            ).total_seconds()

            if elapsed <= 0:
                previous = record
                continue

            disk_read_delta = (
                record.disk_read_bytes - previous.disk_read_bytes
            )

            disk_write_delta = (
                record.disk_write_bytes - previous.disk_write_bytes
            )

            network_send_delta = (
                record.network_bytes_sent
                - previous.network_bytes_sent
            )

            network_receive_delta = (
                record.network_bytes_received
                - previous.network_bytes_received
            )

            # Counter resets are treated as zero-rate intervals.
            disk_read_rate = max(0, disk_read_delta) / elapsed
            disk_write_rate = max(0, disk_write_delta) / elapsed
            network_send_rate = max(0, network_send_delta) / elapsed
            network_receive_rate = max(0, network_receive_delta) / elapsed

            processed.append(
                ProcessedTelemetry(
                    timestamp=record.timestamp,
                    cpu_percent=record.cpu_percent,
                    memory_percent=record.memory_percent,
                    swap_percent=record.swap_percent,
                    disk_percent=record.disk_percent,
                    load_1m=record.load_1m,
                    process_count=record.process_count,
                    disk_read_rate=disk_read_rate,
                    disk_write_rate=disk_write_rate,
                    network_send_rate=network_send_rate,
                    network_receive_rate=network_receive_rate,
                    top_cpu_process=record.top_cpu_process,
                    top_memory_process=record.top_memory_process,
                )
            )

            previous = record

        return processed
