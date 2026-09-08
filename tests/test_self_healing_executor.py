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


def test_approved_allowed_action_is_executed():
    executor = SelfHealingExecutor()

    action = create_action("clear_cache")

    result = executor.execute(action)

    assert result == "Cache clearing action executed."


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
