from datetime import datetime, timezone
from pathlib import Path

from src.self_healing.audit_repository import HealingAuditRepository
from src.self_healing.models import HealingAction
from src.self_healing.workflow import SelfHealingWorkflow
from src.recommendations.models import Recommendation


def create_recommendation():
    return Recommendation(
        timestamp=datetime.now(timezone.utc),
        metric="disk_percent",
        severity="high",
        title="High disk usage detected",
        description="Disk usage is approaching the configured threshold.",
        suggested_action="Clear user cache",
    )


def test_approved_action_executes_and_is_audited(tmp_path, monkeypatch):
    """Approved cache-cleanup actions should execute and be audited."""

    # NEW: Create an isolated fake home directory.
    fake_home = tmp_path / "home"
    fake_home.mkdir()

    test_cache = fake_home / ".cache"
    test_cache.mkdir()

    # NEW: Make Path.home() return the isolated test home.
    monkeypatch.setattr(Path, "home", lambda: fake_home)

    workflow = SelfHealingWorkflow()

    workflow.audit_repository = HealingAuditRepository(
        database_path=tmp_path / "test.db"
    )

    # NEW: Use the isolated approved cache directory.
    workflow.executor.CACHE_DIRECTORY = test_cache

    # NEW: Create a safe test cache file.
    test_file = test_cache / "test_cache.txt"
    test_file.write_text("temporary cache data")

    recommendation = create_recommendation()

    action = workflow.create_action(recommendation)

    assert action is not None
    assert action.status == "pending"
    assert action.action == "clear_cache"

    workflow.approve(action)

    audit = workflow.execute(action)

    assert audit.approval_status == "approved"
    assert audit.execution_status == "success"
    assert "Cache cleanup completed successfully." in audit.result
    assert not test_file.exists()


def test_rejected_action_is_audited(tmp_path):
    """Rejected healing actions should be audited without execution."""

    workflow = SelfHealingWorkflow()

    workflow.audit_repository = HealingAuditRepository(
        database_path=tmp_path / "test.db"
    )

    recommendation = create_recommendation()

    action = workflow.create_action(recommendation)

    assert action is not None
    assert action.status == "pending"

    workflow.reject(action)

    audits = workflow.audit_repository.get_all()
    assert len(audits) == 1
    audit = audits[0]

    assert audit.approval_status == "rejected"
    assert audit.execution_status == "not_executed"
    assert audit.result == "Healing action rejected by human operator."


def test_unapproved_action_execution_is_audited_as_failed(tmp_path):
    """Execution without approval should be rejected and audited as failed."""

    workflow = SelfHealingWorkflow()

    workflow.audit_repository = HealingAuditRepository(
        database_path=tmp_path / "test.db"
    )

    recommendation = create_recommendation()

    action = workflow.create_action(recommendation)

    assert action is not None
    assert action.status == "pending"

    audit = workflow.execute(action)

    assert audit.approval_status == "pending"
    assert audit.execution_status == "failed"
    assert audit.result == "Healing action execution failed."
    assert audit.error is not None
