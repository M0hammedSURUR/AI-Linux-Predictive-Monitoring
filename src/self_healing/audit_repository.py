from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from src.database.database import (
    get_connection,
    CREATE_HEALING_AUDIT_TABLE,  # NEW
    CREATE_HEALING_AUDIT_TIMESTAMP_INDEX,  # NEW
)
from src.self_healing.audit import HealingAuditLog


class HealingAuditRepository:
    """Provides persistence operations for self-healing audit logs."""

    def __init__(self, database_path: Path | None = None):
        self.database_path = database_path

        # NEW: Ensure custom databases contain the audit table.
        if self.database_path is not None:
            self._initialize_custom_database()

    # NEW: Initialize the audit schema for custom database paths.
    def _initialize_custom_database(self) -> None:
        """Create required audit tables for a custom database."""

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with sqlite3.connect(self.database_path) as connection:
            connection.execute(CREATE_HEALING_AUDIT_TABLE)
            connection.execute(CREATE_HEALING_AUDIT_TIMESTAMP_INDEX)
            connection.commit()

    def save(self, audit: HealingAuditLog) -> None:
        """Store one self-healing audit log."""

        query = """
        INSERT INTO healing_audit_logs (
            timestamp,
            metric,
            action,
            approval_status,
            execution_status,
            result,
            error,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        created_at = datetime.now(timezone.utc).isoformat()

        values = (
            audit.timestamp.isoformat(),
            audit.metric,
            audit.action,
            audit.approval_status,
            audit.execution_status,
            audit.result,
            audit.error,
            created_at,
        )

        if self.database_path is None:
            with get_connection() as connection:
                connection.execute(query, values)
                connection.commit()
            return

        with sqlite3.connect(self.database_path) as connection:
            connection.execute(query, values)
            connection.commit()

    def get_all(self) -> list[HealingAuditLog]:
        """Load all self-healing audit logs."""

        query = """
        SELECT
            timestamp,
            metric,
            action,
            approval_status,
            execution_status,
            result,
            error
        FROM healing_audit_logs
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
            HealingAuditLog(
                timestamp=datetime.fromisoformat(row["timestamp"]),
                metric=row["metric"],
                action=row["action"],
                approval_status=row["approval_status"],
                execution_status=row["execution_status"],
                result=row["result"],
                error=row["error"],
            )
            for row in rows
        ]
