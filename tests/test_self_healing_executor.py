from datetime import datetime, timezone

import pytest

from src.self_healing.executor import SelfHealingExecutor
from src.self_healing.models import HealingAction


def create_action(action: str, status: str = "approved"):
    return HealingAction(
        timestamp=datetime.now(timezone.utc),
        metric="cpu_percent",
        action=action,
        reason="Test healing action",
        status=status,
    )


def test_approved_allowed_action_is_executed(tmp_path):
    """Approved cache cleanup should remove only temporary test contents."""

    executor = SelfHealingExecutor()

    # NEW: Use a temporary directory instead of the real ~/.cache
    test_cache = tmp_path / ".cache"
    test_cache.mkdir()

    # NEW: Create files and a subdirectory for the cleanup test
    test_file = test_cache / "test_file.txt"
    test_file.write_text("test cache data")

    test_directory = test_cache / "test_directory"
    test_directory.mkdir()

    nested_file = test_directory / "nested.txt"
    nested_file.write_text("nested cache data")

    # NEW: Redirect the executor to the temporary test cache
    executor.CACHE_DIRECTORY = test_cache

    action = create_action("clear_cache")

    result = executor.execute(action)

    # NEW: Verify cleanup succeeded
    assert "Cache cleanup completed successfully." in result
    assert not test_file.exists()
    assert not test_directory.exists()

    # NEW: The cache directory itself must remain
    assert test_cache.exists()
    assert test_cache.is_dir()


def test_unapproved_action_cannot_be_executed():
    executor = SelfHealingExecutor()

    action = create_action(
        "clear_cache",
        status="pending",
    )

    with pytest.raises(ValueError):
        executor.execute(action)


def test_unknown_action_is_blocked():
    executor = SelfHealingExecutor()

    action = create_action(
        "delete_everything",
    )

    with pytest.raises(ValueError):
        executor.execute(action)


def test_arbitrary_command_is_blocked():
    executor = SelfHealingExecutor()

    action = create_action(
        "rm -rf /",
    )

    with pytest.raises(ValueError):
        executor.execute(action)


# NEW: Real service restart must remain disabled for now
def test_real_service_restart_is_not_implemented():
    executor = SelfHealingExecutor()

    action = create_action("restart_service")

    with pytest.raises(ValueError, match="Real service restart is not implemented yet"):
        executor.execute(action)
