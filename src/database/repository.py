from pathlib import Path

from src.collector.models import TelemetryRecord
from src.database.database import get_connection


class TelemetryRepository:
    """Provides persistence operations for telemetry records."""

    def __init__(self, database_path: Path | None = None):
        self.database_path = database_path

    def save(self, record: TelemetryRecord) -> None:
        """Store one telemetry record in the database."""

        query = """
        INSERT INTO telemetry (
            timestamp,
            cpu_percent,
            memory_percent,
            swap_percent,
            disk_percent,
            load_1m,
            disk_read_bytes,
            disk_write_bytes,
            network_bytes_sent,
            network_bytes_received,
            process_count,
            top_cpu_process,
            top_memory_process
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        values = (
            record.timestamp.isoformat(),
            record.cpu_percent,
            record.memory_percent,
            record.swap_percent,
            record.disk_percent,
            record.load_1m,
            record.disk_read_bytes,
            record.disk_write_bytes,
            record.network_bytes_sent,
            record.network_bytes_received,
            record.process_count,
            record.top_cpu_process,
            record.top_memory_process,
        )

        if self.database_path is None:
            with get_connection() as connection:
                connection.execute(query, values)
                connection.commit()
            return

        import sqlite3

        with sqlite3.connect(self.database_path) as connection:
            connection.execute(query, values)
            connection.commit()
