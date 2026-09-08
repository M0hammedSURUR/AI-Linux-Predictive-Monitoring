from datetime import datetime, timezone

from src.self_healing.audit import HealingAuditLog
from src.self_healing.audit_repository import HealingAuditRepository


def test_audit_log_can_be_saved_and_loaded(tmp_path):
    database_path = tmp_path / "test.db"

    # Create the database schema
    from src.database.database import (
        CREATE_HEALING_AUDIT_TABLE,
        CREATE_HEALING_AUDIT_TIMESTAMP_INDEX,
    )

    import sqlite3

    with sqlite3.connect(database_path) as connection:
        connection.execute(CREATE_HEALING_AUDIT_TABLE)
        connection.execute(CREATE_HEALING_AUDIT_TIMESTAMP_INDEX)
        connection.commit()

    repository = HealingAuditRepository(database_path)

    audit = HealingAuditLog(
        timestamp=datetime.now(timezone.utc),
        metric="cpu_percent",
        action="restart_service",
        approval_status="approved",
        execution_status="success",
        result="Service restart action executed.",
    )

    repository.save(audit)

    logs = repository.get_all()

    assert len(logs) == 1
    assert logs[0].metric == "cpu_percent"
    assert logs[0].action == "restart_service"
    assert logs[0].approval_status == "approved"
    assert logs[0].execution_status == "success"
    assert logs[0].error is None
