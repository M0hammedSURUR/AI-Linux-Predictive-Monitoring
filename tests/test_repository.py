import sqlite3
from datetime import datetime, timezone

from src.collector.models import TelemetryRecord
from src.database.repository import TelemetryRepository


def test_telemetry_record_can_be_saved(tmp_path):
    database_path = tmp_path / "test_monitoring.db"

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    connection.execute(
        """
        CREATE TABLE telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            cpu_percent REAL NOT NULL,
            memory_percent REAL NOT NULL,
            swap_percent REAL NOT NULL,
            disk_percent REAL NOT NULL,
            load_1m REAL NOT NULL,
            disk_read_bytes INTEGER NOT NULL,
            disk_write_bytes INTEGER NOT NULL,
            network_bytes_sent INTEGER NOT NULL,
            network_bytes_received INTEGER NOT NULL,
            process_count INTEGER NOT NULL,
            top_cpu_process TEXT,
            top_memory_process TEXT
        )
        """
    )

    connection.commit()
    connection.close()

    record = TelemetryRecord(
        timestamp=datetime.now(timezone.utc),
        cpu_percent=25.0,
        memory_percent=40.0,
        swap_percent=0.0,
        disk_percent=50.0,
        load_1m=1.5,
        disk_read_bytes=1000,
        disk_write_bytes=2000,
        network_bytes_sent=3000,
        network_bytes_received=4000,
        process_count=100,
        top_cpu_process="test_cpu_process",
        top_memory_process="test_memory_process",
    )

    repository = TelemetryRepository(database_path)
    repository.save(record)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    row = connection.execute(
        """
        SELECT *
        FROM telemetry
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    connection.close()

    assert row is not None
    assert row["cpu_percent"] == 25.0
    assert row["memory_percent"] == 40.0
    assert row["process_count"] == 100
    assert row["top_cpu_process"] == "test_cpu_process"
    assert row["top_memory_process"] == "test_memory_process"
