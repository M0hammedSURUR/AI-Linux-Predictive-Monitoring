import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "data" / "monitoring.db"


CREATE_TELEMETRY_TABLE = """
CREATE TABLE IF NOT EXISTS telemetry (
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
);
"""


CREATE_TIMESTAMP_INDEX = """
CREATE INDEX IF NOT EXISTS idx_telemetry_timestamp
ON telemetry(timestamp);
"""


# ==================== DAY 11: ADDED ====================
# Stores detected anomaly events separately from raw telemetry.
CREATE_ANOMALY_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS anomaly_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    is_anomaly INTEGER NOT NULL,
    severity TEXT NOT NULL,
    reasons TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""
# =======================================================


def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite database connection."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database() -> None:
    """Create the database tables and indexes if they do not exist."""
    with get_connection() as connection:
        connection.execute(CREATE_TELEMETRY_TABLE)
        connection.execute(CREATE_TIMESTAMP_INDEX)

        # ==================== DAY 11: ADDED ====================
        connection.execute(CREATE_ANOMALY_EVENTS_TABLE)
        # =======================================================

        connection.commit()
