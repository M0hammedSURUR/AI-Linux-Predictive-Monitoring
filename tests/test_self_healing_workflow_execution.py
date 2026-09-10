from datetime import datetime, timezone

from src.recommendations.models import Recommendation
from src.self_healing.workflow import SelfHealingWorkflow


def create_recommendation():
    """Create a sample disk recommendation for testing."""

    return Recommendation(
        timestamp=datetime.now(timezone.utc),
        metric="disk_percent",  # NEW: Maps to the implemented clear_cache action
        severity="high",
        title="High Disk Usage",
        description="Disk usage is above the configured threshold.",
        suggested_action="Check disk usage and identify large files.",
    )


def test_approved_action_executes_and_is_audited(tmp_path):
    """Approved cache-cleanup actions should execute and be audited."""

    workflow = SelfHealingWorkflow()

    from src.self_healing.audit_repository import HealingAuditRepository

    workflow.audit_repository = HealingAuditRepository(
        database_path=tmp_path / "test.db"
    )

    # NEW: Use a temporary cache directory instead of the real ~/.cache
    workflow.executor.CACHE_DIRECTORY = tmp_path / ".cache"
    workflow.executor.CACHE_DIRECTORY.mkdir()

    # NEW: Create a safe test cache file
    test_file = workflow.executor.CACHE_DIRECTORY / "test_cache.txt"
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
    assert audit.error is None

    # NEW: Verify the test cache content was actually removed
    assert not test_file.exists()

    logs = workflow.audit_repository.get_all()

    assert len(logs) == 1
    assert logs[0].execution_status == "success"


def test_rejected_action_is_audited(tmp_path):
    """Rejected actions should be recorded without execution."""

    workflow = SelfHealingWorkflow()

    from src.self_healing.audit_repository import HealingAuditRepository

    workflow.audit_repository = HealingAuditRepository(
        database_path=tmp_path / "test.db"
    )

    recommendation = create_recommendation()

    action = workflow.create_action(recommendation)

    assert action is not None

    workflow.reject(action)

    logs = workflow.audit_repository.get_all()

    assert len(logs) == 1
    assert logs[0].approval_status == "rejected"
    assert logs[0].execution_status == "not_executed"


def test_unapproved_action_execution_is_audited_as_failed(tmp_path):
    """Execution of an unapproved action should fail safely."""

    workflow = SelfHealingWorkflow()

    from src.self_healing.audit_repository import HealingAuditRepository

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
    assert audit.error is not None

    logs = workflow.audit_repository.get_all()

    assert len(logs) == 1
    assert logs[0].execution_status == "failed"
