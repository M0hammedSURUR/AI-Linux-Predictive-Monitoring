from datetime import datetime, timezone

from src.recommendations.models import Recommendation
from src.self_healing.models import HealingAction
from src.self_healing.workflow import SelfHealingWorkflow


def create_recommendation():
    return Recommendation(
        timestamp=datetime.now(timezone.utc),
        metric="cpu_percent",
        severity="high",
        title="High CPU Usage",
        description="CPU usage is above the configured threshold.",
        suggested_action="Investigate the responsible process.",
    )


def test_recommendation_creates_pending_healing_action():
    workflow = SelfHealingWorkflow()

    action = workflow.create_action(
        create_recommendation()
    )

    assert isinstance(action, HealingAction)
    assert action is not None
    assert action.metric == "cpu_percent"
    assert action.action == "restart_service"
    assert action.status == "pending"


def test_pending_action_can_be_approved():
    workflow = SelfHealingWorkflow()

    action = workflow.create_action(
        create_recommendation()
    )

    approved_action = workflow.approve(action)

    assert approved_action.status == "approved"


def test_pending_action_can_be_rejected():
    workflow = SelfHealingWorkflow()

    action = workflow.create_action(
        create_recommendation()
    )

    rejected_action = workflow.reject(action)

    assert rejected_action.status == "rejected"


def test_unknown_metric_does_not_create_action():
    workflow = SelfHealingWorkflow()

    recommendation = Recommendation(
        timestamp=datetime.now(timezone.utc),
        metric="unknown_metric",
        severity="high",
        title="Unknown",
        description="Unknown condition.",
        suggested_action="Unknown action.",
    )

    action = workflow.create_action(recommendation)

    assert action is None
