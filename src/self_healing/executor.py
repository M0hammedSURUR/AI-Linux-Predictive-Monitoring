from src.self_healing.models import HealingAction


class SelfHealingExecutor:
    """Executes only predefined, approved healing actions."""

    # NEW: Whitelist of actions that the executor is allowed to perform
    ALLOWED_ACTIONS = {
        "clear_cache",
        "restart_service",
    }

    def execute(self, action: HealingAction) -> str:
        """Execute an approved healing action."""

        # NEW: Only approved actions can be executed
        if action.status != "approved":
            raise ValueError(
                "Only approved healing actions can be executed."
            )

        # NEW: Block actions that are not explicitly whitelisted
        if action.action not in self.ALLOWED_ACTIONS:
            raise ValueError(
                f"Action '{action.action}' is not allowed."
            )

        # NEW: Safe placeholder execution
        # Actual Linux commands will be implemented later.
        if action.action == "clear_cache":
            return "Cache clearing action executed."

        if action.action == "restart_service":
            return "Service restart action executed."

        # NEW: Defensive fallback
        raise ValueError(
            f"Unsupported healing action: {action.action}"
        )
