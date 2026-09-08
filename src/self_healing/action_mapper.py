from src.recommendations.models import Recommendation


class HealingActionMapper:
    """Maps recommendations to predefined healing actions."""

    # NEW: Explicit mapping between monitored metrics and safe actions
    ACTION_MAP = {
        "cpu_percent": "restart_service",
        "memory_percent": "restart_service",
        "disk_percent": "clear_cache",
    }

    def map(self, recommendation: Recommendation) -> str | None:
        """Return a predefined healing action for a recommendation."""

        # NEW: Never create an executable action if no mapping exists
        return self.ACTION_MAP.get(recommendation.metric)
