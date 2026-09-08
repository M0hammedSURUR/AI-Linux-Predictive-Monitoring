from datetime import datetime, timezone

from src.self_healing.engine import SelfHealingEngine
from src.self_healing.models import HealingAction


def create_action() -> HealingAction:
    """Create a sample healing action."""

    return HealingAction(
        timestamp=datetime.now(timezone.utc),
        metric="cpu_percent",
        action="Investigate high CPU process",
        reason="CPU usage exceeded the configured threshold.",
        status="pending",
    )


def test_pending_action_can_be_approved():
    """Verify that a pending action can be approved."""

    engine = SelfHealingEngine()
    action = create_action()

    result = engine.approve(action)

    assert result.status == "approved"


def test_pending_action_can_be_rejected():
    """Verify that a pending action can be rejected."""

    engine = SelfHealingEngine()
    action = create_action()

    result = engine.reject(action)

    assert result.status == "rejected"


def test_approved_action_cannot_be_approved_again():
    """Verify that an approved action cannot be approved again."""

    engine = SelfHealingEngine()
    action = create_action()

    engine.approve(action)

    try:
        engine.approve(action)
        assert False
    except ValueError:
        pass


def test_rejected_action_cannot_be_rejected_again():
    """Verify that a rejected action cannot be rejected again."""

    engine = SelfHealingEngine()
    action = create_action()

    engine.reject(action)

    try:
        engine.reject(action)
        assert False
    except ValueError:
        pass
