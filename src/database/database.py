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

CREATE_PREDICTION_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS prediction_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,

    metric TEXT NOT NULL,
    current_value REAL NOT NULL,
    predicted_value REAL NOT NULL,
    threshold REAL NOT NULL,

    risk_level TEXT NOT NULL,
    message TEXT NOT NULL,

    created_at TEXT NOT NULL
);
"""

CREATE_PREDICTION_TIMESTAMP_INDEX = """
CREATE INDEX IF NOT EXISTS idx_prediction_events_timestamp
ON prediction_events(timestamp);
"""

# NEW: Persistent self-healing audit table
CREATE_HEALING_AUDIT_TABLE = """
CREATE TABLE IF NOT EXISTS healing_audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,

    metric TEXT NOT NULL,
    action TEXT NOT NULL,

    approval_status TEXT NOT NULL,
    execution_status TEXT NOT NULL,

    result TEXT NOT NULL,
    error TEXT,

    created_at TEXT NOT NULL
);
"""

# NEW: Index for chronological audit-log queries
CREATE_HEALING_AUDIT_TIMESTAMP_INDEX = """
CREATE INDEX IF NOT EXISTS idx_healing_audit_timestamp
ON healing_audit_logs(timestamp);
"""


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

        connection.execute(CREATE_PREDICTION_EVENTS_TABLE)
        connection.execute(CREATE_PREDICTION_TIMESTAMP_INDEX)

        # NEW: Create self-healing audit storage
        connection.execute(CREATE_HEALING_AUDIT_TABLE)
        connection.execute(CREATE_HEALING_AUDIT_TIMESTAMP_INDEX)

        connection.commit()
