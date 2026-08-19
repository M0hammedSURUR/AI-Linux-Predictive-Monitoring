from datetime import datetime, timezone

from src.anomaly_detection.events import AnomalyEvent
from src.database.repository import TelemetryRepository


def test_anomaly_event_creation():
    """Verify that an anomaly event can be created."""

    now = datetime.now(timezone.utc)

    event = AnomalyEvent(
        timestamp=now,
        is_anomaly=True,
        severity="high",
        reasons=[
            "High CPU usage",
            "High memory usage",
        ],
        created_at=now,
    )

    assert event.timestamp == now
    assert event.is_anomaly is True
    assert event.severity == "high"
    assert len(event.reasons) == 2
    assert event.created_at == now


# ==================== DAY 11: ADDED ====================

def test_anomaly_event_can_be_saved(tmp_path):
    """Verify that an anomaly event can be stored in SQLite."""

    database_path = tmp_path / "test_monitoring.db"

    # Create the required anomaly_events table.
    import sqlite3

    connection = sqlite3.connect(database_path)

    connection.execute(
        """
        CREATE TABLE anomaly_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            is_anomaly INTEGER NOT NULL,
            severity TEXT NOT NULL,
            reasons TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()

    now = datetime.now(timezone.utc)

    event = AnomalyEvent(
        timestamp=now,
        is_anomaly=True,
        severity="high",
        reasons=[
            "High CPU usage",
            "High memory usage",
        ],
        created_at=now,
    )

    repository = TelemetryRepository(database_path)

    repository.save_anomaly_event(event)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    row = connection.execute(
        """
        SELECT
            timestamp,
            is_anomaly,
            severity,
            reasons,
            created_at
        FROM anomaly_events
        """
    ).fetchone()

    connection.close()

    assert row is not None
    assert row["timestamp"] == now.isoformat()
    assert row["is_anomaly"] == 1
    assert row["severity"] == "high"
    assert row["reasons"] == "High CPU usage | High memory usage"
    assert row["created_at"] == now.isoformat()

# =======================================================
