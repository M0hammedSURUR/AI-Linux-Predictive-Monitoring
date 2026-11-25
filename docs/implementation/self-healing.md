# Self-Healing Implementation

## 1. Overview

The self-healing module provides a controlled mechanism for responding to detected or predicted Linux system issues.

The system follows a **human-approved self-healing** approach. A healing action is first proposed based on a recommendation, then explicitly approved or rejected by the human operator.

Only predefined healing actions are permitted. Both real execution and simulation require human approval.

## 2. Self-Healing Workflow

The self-healing workflow consists of the following stages:

1. Monitoring data is collected from the Linux system.
2. Anomaly detection and prediction identify potential problems.
3. The recommendation engine proposes a suitable action.
4. The action mapper converts the recommendation into a predefined healing action.
5. The action is created with `pending` status.
6. The human operator approves or rejects the action.
7. The workflow checks the approval status before execution or simulation.
8. The executor validates the action and execution target for real execution.
9. The executor performs the predefined action.
10. Execution duration and result are evaluated.
11. The execution result or simulation result is recorded in the healing audit log.

## 3. Human Approval

Human approval is mandatory before a healing action can be executed or simulated.

Supported action states are:

- `pending`
- `approved`
- `rejected`

Only actions with `approved` status can proceed.

If a pending or rejected action is submitted for execution or simulation:

- The operation is blocked.
- No real system action is performed.
- The attempt is recorded in the audit log with `failed` execution status.
- The error message indicates that approval is required.

Rejected actions are separately recorded with `not_executed` status.

This enforcement is performed in the workflow before the simulation branch, preventing simulation mode from bypassing human approval.

## 4. Action Mapping

The current action mapping is:

| Monitoring Metric | Healing Action |
| ----------------- | -------------- |
| `cpu_percent` | `restart_service` |
| `memory_percent` | `restart_service` |
| `disk_percent` | `clear_cache` |

The `clear_cache` action is currently implemented as the first real Linux healing action.

The `restart_service` action is included in the predefined allow-list but is intentionally not implemented. The executor rejects attempts to perform a real service restart with a controlled error.

## 5. Safety Policy

The self-healing executor and workflow follow these restrictions:

- Only predefined actions are allowed.
- Arbitrary shell commands cannot be supplied by the user.
- Arbitrary filesystem paths cannot be supplied by the healing recommendation.
- `clear_cache` operates only on the current user's cache directory.
- The cache directory is resolved before execution.
- The resolved execution target must exactly match the approved `~/.cache` directory.
- Cache cleanup cannot be redirected to another filesystem location through the configured target.
- The cache directory itself is not deleted.
- Symbolic links are not followed as directories during recursive cleanup.
- No `sudo` or elevated privileges are used.
- Human approval is required for real execution and simulation.
- Unsupported actions are rejected.
- Unimplemented service restart operations are rejected safely.
- Simulation mode never invokes the real system executor.

## 6. Real Cache Cleanup

The first real healing action is:

```text
clear_cache
```

The executor targets:

```text
~/.cache
```

Before cleanup, the executor resolves the configured target and compares it with the resolved current user's approved cache directory.

If the target does not exactly match the approved cache directory, execution is rejected.

The action removes the contents inside the approved cache directory while preserving the cache directory itself.

Directories are removed recursively. Symbolic links are treated as links rather than followed as directories.

The implementation counts successfully removed top-level items and tracks items that could not be removed. If individual cleanup operations fail, a controlled `RuntimeError` is raised to report the partial failure.

## 7. Execution and Error Handling

The executor verifies that:

1. The healing action is approved.
2. The action is included in the allowed action list.
3. The requested action has an implemented execution path.
4. The target cache directory is exactly the approved `~/.cache` directory.
5. The target cache directory exists.
6. The target path is a directory.

Unsupported or unimplemented actions result in controlled errors instead of arbitrary execution.

For example, `restart_service` currently returns a controlled error because real service restart functionality has not yet been implemented.

### Execution Duration Monitoring

The executor measures the duration of an approved healing action using a monotonic timer.

The configured execution-duration threshold is:

```text
10 seconds
```

If the completed operation takes longer than the configured threshold, the executor raises a `TimeoutError`.

This implementation is a **post-execution duration check**. It does not forcibly terminate a filesystem operation while it is running.

This approach provides execution-duration monitoring without attempting unsafe termination of an active filesystem operation.

### Workflow Error Handling

The workflow catches execution exceptions and records them in the audit log.

This includes:

- Invalid or unsupported actions.
- Unimplemented actions.
- Execution timeouts.
- Partial cache-cleanup failures.
- Other execution exceptions.

Failed attempts are recorded with `failed` execution status and the corresponding error message.

## 8. Simulation Mode

Simulation mode allows the workflow to demonstrate a proposed healing operation without changing the actual Linux system.

The workflow first verifies that the action has `approved` status.

If approval is valid:

- The real executor is not called.
- No cache cleanup or service operation is performed.
- The audit log records the execution status as `simulated`.
- The result confirms that no real system action was executed.

Example simulation result:

```text
Simulation completed successfully. No real system action was executed.
```

Simulation is useful for demonstrations and testing potentially risky healing workflows without performing real system modifications.

## 9. Healing Audit Log

Healing decisions and execution attempts are recorded in SQLite.

The `healing_audit_logs` table stores:

- timestamp
- metric
- action
- approval status
- execution status
- result
- error information
- record creation time

The workflow records:

| Situation | Audit Execution Status |
| --------- | ---------------------- |
| Successful real execution | `success` |
| Failed real execution | `failed` |
| Rejected action | `not_executed` |
| Approved simulation | `simulated` |
| Execution attempt without approval | `failed` |

This provides traceability for rejected actions, execution attempts, successful operations, and simulations.

## 10. Real Linux Execution Test

The real `clear_cache` action was tested through the dashboard after human approval.

The first successful execution produced:

```text
Cache cleanup completed successfully.
21 items removed from /home/msr4/.cache.
```

A subsequent execution produced:

```text
Cache cleanup completed successfully.
0 items removed from /home/msr4/.cache.
```

The second result occurred because the cache contents had already been cleaned.

These are historical real execution results, separate from simulation testing.

## 11. Simulation Verification

The simulation workflow was tested using a controlled disk-usage prediction scenario:

| Parameter | Test Value |
| --------- | ---------- |
| Current disk usage | 85% |
| Predicted disk usage | 95% |
| Configured threshold | 90% |
| Proposed action | `clear_cache` |
| Human approval | Approved |
| Execution status | `simulated` |

The result was:

```text
Simulation completed successfully. No real system action was executed.
```

This verified that the dashboard could demonstrate an approved healing action without performing real cache cleanup.

## 12. Audit Verification

Historical SQLite audit records confirmed real execution and rejection behaviour.

Example records:

```text
disk_percent | clear_cache     | approved | success       | 21 items removed
disk_percent | clear_cache     | approved | success       | 0 items removed
cpu_percent  | restart_service | approved | failed        | Healing action execution failed
cpu_percent  | restart_service | rejected | not_executed  | Healing action rejected by human operator
```

Additional automated tests verify that pending and rejected actions cannot bypass



13. Testing

The self-healing executor and workflow are covered by automated tests.

The executor tests verify:

Approved actions can execute.

Unapproved actions are blocked.

Unknown actions are blocked.

Arbitrary commands are blocked.

Service restart is safely rejected because it is not implemented.

The execution-duration threshold is configured.

Cache cleanup removes test data.

Unsafe cache targets are rejected.

The workflow tests verify:

Approved actions execute successfully.

Successful execution is audited.

Rejected actions are audited as not_executed.

Unapproved execution attempts are audited as failed.

Pending actions cannot enter simulation.

Rejected actions cannot enter simulation.

Execution timeouts are recorded in the audit log.

Latest Verification Results

Complete project test suite:

72 passed

Compilation checks:

python -m py_compile src/self_healing/workflow.py
python -m py_compile src/dashboard/app.py

Both compilation checks completed successfully.

14. Current Implementation Status

Component

Status

Human approval

Implemented

Approval enforcement in real execution

Implemented

Approval enforcement in simulation

Implemented

Action mapping

Implemented

Healing executor

Implemented

Real clear_cache

Implemented

Simulation mode

Implemented

Audit logging

Implemented

Execution success tracking

Implemented

Execution failure tracking

Implemented

Rejection tracking

Implemented

Timeout error auditing

Implemented

Strict cache target validation

Implemented

Execution duration monitoring

Implemented

Real Linux execution test

Completed

Simulation verification

Completed

restart_service

Not implemented

Multiple healing actions

Future enhancement

15. Future Improvements

Future versions can add additional controlled healing actions such as:

Safe service restart.

Temporary-file cleanup.

Resource-aware process management.

Configurable safety policies.

Stronger rollback mechanisms.

Multi-server healing support.

All future actions should preserve the project's human-approval and safety-first design.
