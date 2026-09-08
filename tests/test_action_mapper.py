from datetime import datetime, timezone

from src.recommendations.models import Recommendation
from src.self_healing.action_mapper import HealingActionMapper


def create_recommendation(metric: str):
    return Recommendation(
        timestamp=datetime.now(timezone.utc),
        metric=metric,
        severity="high",
        title="Test Recommendation",
        description="Test recommendation",
        suggested_action="Test suggested action",
    )


def test_cpu_recommendation_maps_to_restart_service():
    mapper = HealingActionMapper()

    action = mapper.map(
        create_recommendation("cpu_percent")
    )

    assert action == "restart_service"


def test_memory_recommendation_maps_to_restart_service():
    mapper = HealingActionMapper()

    action = mapper.map(
        create_recommendation("memory_percent")
    )

    assert action == "restart_service"


def test_disk_recommendation_maps_to_clear_cache():
    mapper = HealingActionMapper()

    action = mapper.map(
        create_recommendation("disk_percent")
    )

    assert action == "clear_cache"


def test_unknown_metric_has_no_healing_action():
    mapper = HealingActionMapper()

    action = mapper.map(
        create_recommendation("unknown_metric")
    )

    assert action is None
