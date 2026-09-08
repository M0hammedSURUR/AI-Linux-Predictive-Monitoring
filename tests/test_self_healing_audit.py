from datetime import datetime, timezone

from src.self_healing.audit import HealingAuditLog


def test_successful_healing_audit_log():
    audit = HealingAuditLog(
        timestamp=datetime.now(timezone.utc),
        metric="cpu_percent",
        action="restart_service",
        approval_status="approved",
        execution_status="success",
        result="Service restart action executed.",
    )

    assert audit.metric == "cpu_percent"
    assert audit.action == "restart_service"
    assert audit.approval_status == "approved"
    assert audit.execution_status == "success"
    assert audit.error is None


def test_failed_healing_audit_log():
    audit = HealingAuditLog(
        timestamp=datetime.now(timezone.utc),
        metric="disk_percent",
        action="clear_cache",
        approval_status="approved",
        execution_status="failed",
        result="",
        error="Execution failed.",
    )

    assert audit.execution_status == "failed"
    assert audit.error == "Execution failed."
