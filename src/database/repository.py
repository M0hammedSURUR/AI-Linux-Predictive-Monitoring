from datetime import datetime
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

    def get_recent_records(
        self,
        limit: int | None = None,
    ) -> list[TelemetryRecord]:
        """Retrieve telemetry records ordered by timestamp."""

        query = """
        SELECT
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
        FROM telemetry
        ORDER BY timestamp ASC
        """

        if limit is not None:
            query += " LIMIT ?"

        if self.database_path is None:
            connection_context = get_connection()
        else:
            import sqlite3

            connection_context = sqlite3.connect(self.database_path)

        with connection_context as connection:
            if limit is not None:
                rows = connection.execute(query, (limit,)).fetchall()
            else:
                rows = connection.execute(query).fetchall()

        return [
            TelemetryRecord(
                timestamp=datetime.fromisoformat(row[0]),
                cpu_percent=row[1],
                memory_percent=row[2],
                swap_percent=row[3],
                disk_percent=row[4],
                load_1m=row[5],
                disk_read_bytes=row[6],
                disk_write_bytes=row[7],
                network_bytes_sent=row[8],
                network_bytes_received=row[9],
                process_count=row[10],
                top_cpu_process=row[11],
                top_memory_process=row[12],
            )
            for row in rows
        ]
