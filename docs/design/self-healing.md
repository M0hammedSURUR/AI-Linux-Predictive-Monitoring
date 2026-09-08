# Human-Approved Self-Healing Design

## 1. Purpose

The Self-Healing component provides a controlled mechanism for
proposing and approving system recovery actions.

The current implementation focuses on the safety and approval
workflow.

It does not execute real system commands.

## 2. Architecture

```text
Anomaly Detection / Prediction
            |
            v
   Recommendation Engine
            |
            v
       HealingAction
          pending
            |
       Human Review
        /        \
       /          \
   Approve       Reject
      |             |
      v             v
  approved       rejected
      |
      v

Future Self-Healing Action
3. HealingAction Model

The HealingAction model represents a proposed recovery action.

Field	Description
timestamp	Time associated with the condition
metric	System metric that triggered the action
action	Proposed recovery action
reason	Explanation for the proposed action
status	Current approval state

The supported states are:

pending
approved
rejected
4. Human Approval Principle

The system follows a human-in-the-loop approach.

A proposed action starts in the pending state.

An administrator can:

Approve the action.
Reject the action.

Only pending actions can transition to another state.

pending → approved
pending → rejected

Once an action has been approved or rejected, the same transition
cannot be performed again.

5. Safety Boundary

The current Self-Healing Engine does not execute operating-system
commands.

It does not automatically:

Stop processes.
Restart services.
Delete files.
Modify configuration.
Execute shell commands.

This prevents an incorrect AI recommendation from directly changing
the Linux system.

6. Software Structure
src/self_healing/
├── __init__.py
├── models.py
└── engine.py
models.py

Defines the HealingAction data model.

engine.py

Contains SelfHealingEngine, which manages approval and rejection
of proposed actions.

7. Testing

The Self-Healing component is tested using unit tests.

The tests verify:

A pending action can be approved.
A pending action can be rejected.
An approved action cannot be approved again.
A rejected action cannot be rejected again.

The Self-Healing test suite passed:

4 passed

The complete project test suite passed:

28 passed
8. Current Limitations

The current implementation represents the approval layer only.

Actual operating-system recovery actions are intentionally not
executed yet.

This allows the project to establish the safety architecture before
introducing privileged system operations.

9. Future Enhancement

Future versions can introduce controlled recovery actions such as:

Restarting a selected service.
Managing a high-resource process.
Performing controlled disk cleanup.
Executing predefined administrative commands.

These actions should only execute after explicit human approval.

Additional safeguards can include:

Command allowlists.
Action timeouts.
Execution logs.
Rollback mechanisms.
Permission checks.
Audit history.
10. Design Benefit

The human-approved architecture provides a clear separation between:

AI Detection
     ↓
AI Recommendation
     ↓
Human Decision
     ↓
System Action

This improves safety, explainability, accountability, and
maintainability.

The architecture also provides the foundation for the final
self-healing functionality of the project.
