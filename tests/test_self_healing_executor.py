from datetime import datetime, timezone
from pathlib import Path

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


def test_approved_allowed_action_is_executed(tmp_path, monkeypatch):
    """Approved cache cleanup should remove only test cache contents."""

    # NEW: Create an isolated fake home directory for this test.
    fake_home = tmp_path / "home"
    fake_home.mkdir()

    test_cache = fake_home / ".cache"
    test_cache.mkdir()

    # NEW: Make Path.home() return the isolated test home.
    monkeypatch.setattr(Path, "home", lambda: fake_home)

    executor = SelfHealingExecutor()

    # NEW: Use the isolated cache directory.
    executor.CACHE_DIRECTORY = test_cache

    test_file = test_cache / "test_file.txt"
    test_file.write_text("test cache data")

    test_directory = test_cache / "test_directory"
    test_directory.mkdir()

    nested_file = test_directory / "nested.txt"
    nested_file.write_text("nested cache data")

    action = create_action("clear_cache")

    result = executor.execute(action)

    assert "Cache cleanup completed successfully." in result
    assert not test_file.exists()
    assert not test_directory.exists()

    # NEW: The cache directory itself must remain.
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


def test_real_service_restart_is_not_implemented():
    executor = SelfHealingExecutor()

    action = create_action("restart_service")

    with pytest.raises(
        ValueError,
        match="Real service restart is not implemented yet",
    ):
        executor.execute(action)


def test_execution_timeout_is_configured():
    executor = SelfHealingExecutor()

    assert executor.EXECUTION_TIMEOUT_SECONDS == 10
    assert executor.EXECUTION_TIMEOUT_SECONDS > 0


# NEW: Prevent cache cleanup from being redirected outside ~/.cache.
def test_cache_cleanup_rejects_unsafe_target(tmp_path):
    executor = SelfHealingExecutor()

    unsafe_directory = tmp_path / "unsafe"
    unsafe_directory.mkdir()

    executor.CACHE_DIRECTORY = unsafe_directory

    action = create_action("clear_cache")

    with pytest.raises(
        ValueError,
        match="outside the approved user cache directory",
    ):
        executor.execute(action)
