from src.recommendations.models import Recommendation
from src.self_healing.action_mapper import HealingActionMapper
from src.self_healing.engine import SelfHealingEngine
from src.self_healing.models import HealingAction
from src.self_healing.executor import SelfHealingExecutor
from src.self_healing.audit import HealingAuditLog
from src.self_healing.audit_repository import HealingAuditRepository


class SelfHealingWorkflow:
    """Coordinates recommendation, approval, execution, and auditing."""

    def __init__(self):
        self.mapper = HealingActionMapper()
        self.approval_engine = SelfHealingEngine()
        self.executor = SelfHealingExecutor()
        self.audit_repository = HealingAuditRepository()

    def create_action(
        self,
        recommendation: Recommendation,
    ) -> HealingAction | None:
        """Convert a recommendation into a pending healing action."""

        action = self.mapper.map(recommendation)

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
        simulation: bool = False,
    ) -> HealingAuditLog:
        """
        Execute an approved action and persist the result.

        In simulation mode, no real system action is executed.
        The simulated execution is still recorded in the audit log.
        """

        if simulation:
            audit = HealingAuditLog(
                timestamp=action.timestamp,
                metric=action.metric,
                action=action.action,
                approval_status=action.status,
                execution_status="simulated",
                result=(
                    "Simulation completed successfully. "
                    "No real system action was executed."
                ),
                error=None,
            )

            self.audit_repository.save(audit)
            return audit

        execution_status = "success"
        result = ""
        error = None

        try:
            result = self.executor.execute(action)

        except ValueError as exc:
            execution_status = "failed"
            error = str(exc)
            result = "Healing action execution failed."

        audit = HealingAuditLog(
            timestamp=action.timestamp,
            metric=action.metric,
            action=action.action,
            approval_status=action.status,
            execution_status=execution_status,
            result=result,
            error=error,
        )

        self.audit_repository.save(audit)

        return audit
