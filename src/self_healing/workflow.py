from src.recommendations.models import Recommendation
from src.self_healing.action_mapper import HealingActionMapper
from src.self_healing.engine import SelfHealingEngine
from src.self_healing.models import HealingAction
from src.self_healing.executor import SelfHealingExecutor  # NEW
from src.self_healing.audit import HealingAuditLog  # NEW
from src.self_healing.audit_repository import HealingAuditRepository  # NEW


class SelfHealingWorkflow:
    """Coordinates recommendation, approval, execution, and auditing."""

    def __init__(self):
        self.mapper = HealingActionMapper()
        self.approval_engine = SelfHealingEngine()
        self.executor = SelfHealingExecutor()  # NEW
        self.audit_repository = HealingAuditRepository()  # NEW

    def create_action(
        self,
        recommendation: Recommendation,
    ) -> HealingAction | None:
        """Convert a recommendation into a pending healing action."""

        # NEW: Map the recommendation to a predefined action
        action = self.mapper.map(recommendation)

        # NEW: Do not create an action without a safe mapping
        if action is None:
            return None

        return HealingAction(
            timestamp=recommendation.timestamp,
            metric=recommendation.metric,
            action=action,
            reason=recommendation.description,
            status="pending",
        )

    def approve(
        self,
        action: HealingAction,
    ) -> HealingAction:
        """Approve a pending healing action."""

        return self.approval_engine.approve(action)

    def reject(
        self,
        action: HealingAction,
    ) -> HealingAction:
        """Reject a pending healing action."""

        result = self.approval_engine.reject(action)

        # NEW: Record rejected actions in the audit log
        audit = HealingAuditLog(
            timestamp=action.timestamp,
            metric=action.metric,
            action=action.action,
            approval_status="rejected",
            execution_status="not_executed",
            result="Healing action rejected by human operator.",
            error=None,
        )

        self.audit_repository.save(audit)

        return result

    def execute(
        self,
        action: HealingAction,
    ) -> HealingAuditLog:
        """Execute an approved action and persist the result."""

        # NEW: Track execution status and result
        execution_status = "success"
        result = ""
        error = None

        try:
            # NEW: Executor enforces approval and action whitelist
            result = self.executor.execute(action)

        except ValueError as exc:
            # NEW: Record failed execution attempts
            execution_status = "failed"
            error = str(exc)
            result = "Healing action execution failed."

        # NEW: Create persistent audit record
        audit = HealingAuditLog(
            timestamp=action.timestamp,
            metric=action.metric,
            action=action.action,
            approval_status=action.status,
            execution_status=execution_status,
            result=result,
            error=error,
        )

        # NEW: Persist the audit record in SQLite
        self.audit_repository.save(audit)

        return audit
