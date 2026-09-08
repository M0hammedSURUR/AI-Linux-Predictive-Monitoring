from src.self_healing.models import HealingAction


class SelfHealingEngine:
    """Controls human approval for proposed healing actions."""

    # NEW: Allowed approval states
    VALID_STATUSES = {"pending", "approved", "rejected"}

    def approve(self, action: HealingAction) -> HealingAction:
        """Approve a proposed healing action."""

        # NEW: Only pending actions can be approved
        if action.status != "pending":
            raise ValueError(
                "Only pending healing actions can be approved."
            )

        action.status = "approved"

        return action

    def reject(self, action: HealingAction) -> HealingAction:
        """Reject a proposed healing action."""

        # NEW: Only pending actions can be rejected
        if action.status != "pending":
            raise ValueError(
                "Only pending healing actions can be rejected."
            )

        action.status = "rejected"

        return action
