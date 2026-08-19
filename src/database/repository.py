from datetime import datetime
from pathlib import Path
import sqlite3

from src.collector.models import TelemetryRecord
from src.anomaly_detection.events import AnomalyEvent
from src.database.database import get_connection


class TelemetryRepository:
    """Provides persistence operations for telemetry and anomaly records."""

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

        with sqlite3.connect(self.database_path) as connection:
            connection.execute(query, values)
            connection.commit()

    def get_all(self) -> list[TelemetryRecord]:
        """Load all telemetry records from the database."""

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
        ORDER BY timestamp
        """

        if self.database_path is None:
            with get_connection() as connection:
                rows = connection.execute(query).fetchall()
        else:
            with sqlite3.connect(self.database_path) as connection:
                connection.row_factory = sqlite3.Row
                rows = connection.execute(query).fetchall()

        return [
            TelemetryRecord(
                timestamp=datetime.fromisoformat(row["timestamp"]),
                cpu_percent=row["cpu_percent"],
                memory_percent=row["memory_percent"],
                swap_percent=row["swap_percent"],
                disk_percent=row["disk_percent"],
                load_1m=row["load_1m"],
                disk_read_bytes=row["disk_read_bytes"],
                disk_write_bytes=row["disk_write_bytes"],
                network_bytes_sent=row["network_bytes_sent"],
                network_bytes_received=row["network_bytes_received"],
                process_count=row["process_count"],
                top_cpu_process=row["top_cpu_process"],
                top_memory_process=row["top_memory_process"],
            )
            for row in rows
        ]

    def get_recent_records(
        self,
        limit: int | None = None,
    ) -> list[TelemetryRecord]:
        """Load recent telemetry records from the database."""

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
        ORDER BY timestamp DESC
        """

        if limit is not None:
            query += " LIMIT ?"

        if self.database_path is None:
            with get_connection() as connection:
                if limit is None:
                    rows = connection.execute(query).fetchall()
                else:
                    rows = connection.execute(query, (limit,)).fetchall()
        else:
            with sqlite3.connect(self.database_path) as connection:
                connection.row_factory = sqlite3.Row

                if limit is None:
                    rows = connection.execute(query).fetchall()
                else:
                    rows = connection.execute(query, (limit,)).fetchall()

        records = [
            TelemetryRecord(
                timestamp=datetime.fromisoformat(row["timestamp"]),
                cpu_percent=row["cpu_percent"],
                memory_percent=row["memory_percent"],
                swap_percent=row["swap_percent"],
                disk_percent=row["disk_percent"],
                load_1m=row["load_1m"],
                disk_read_bytes=row["disk_read_bytes"],
                disk_write_bytes=row["disk_write_bytes"],
                network_bytes_sent=row["network_bytes_sent"],
                network_bytes_received=row["network_bytes_received"],
                process_count=row["process_count"],
                top_cpu_process=row["top_cpu_process"],
                top_memory_process=row["top_memory_process"],
            )
            for row in rows
        ]

        records.reverse()

        return records

    # ==================== DAY 11: ADDED ====================

    def save_anomaly_event(self, event: AnomalyEvent) -> None:
        """Store one anomaly event in the database."""

        query = """
        INSERT INTO anomaly_events (
            timestamp,
            is_anomaly,
            severity,
            reasons,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """

        values = (
            event.timestamp.isoformat(),
            int(event.is_anomaly),
            event.severity,
            " | ".join(event.reasons),
            event.created_at.isoformat(),
        )

        if self.database_path is None:
            with get_connection() as connection:
                connection.execute(query, values)
                connection.commit()
            return

        with sqlite3.connect(self.database_path) as connection:
            connection.execute(query, values)
            connection.commit()

    # =========================================================

