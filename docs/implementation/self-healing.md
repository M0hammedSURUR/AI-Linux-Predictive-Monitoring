# Self-Healing Implementation

## 1. Overview

The self-healing module provides a controlled mechanism for responding to detected or predicted Linux system issues.

The system follows a **human-approved self-healing** approach. A healing action is first proposed based on a recommendation, then explicitly approved or rejected by the human operator before execution.

Only predefined healing actions are permitted.

## 2. Self-Healing Workflow

The self-healing workflow consists of the following stages:

1. Monitoring data is collected from the Linux system.
2. Anomaly detection and prediction identify potential problems.
3. The recommendation engine proposes a suitable action.
4. The action mapper converts the recommendation into a predefined healing action.
5. The action is created with `pending` status.
6. The human operator approves or rejects the action.
7. Only an approved action can reach the executor.
8. The executor validates the action and execution target.
9. The executor performs the predefined action.
10. Execution duration and result are evaluated.
11. The execution result is recorded in the healing audit log.

## 3. Human Approval

Human approval is mandatory before a healing action can be executed.

Supported action states are:

* `pending`
* `approved`
* `rejected`

An action cannot be executed while it is pending or rejected.

This prevents automatic execution of potentially disruptive system operations.

## 4. Action Mapping

The current action mapping is:

| Monitoring Metric | Healing Action    |
| ----------------- | ----------------- |
| `cpu_percent`     | `restart_service` |
| `memory_percent`  | `restart_service` |
| `disk_percent`    | `clear_cache`     |

The `clear_cache` action is currently implemented as the first real Linux healing action.

The `restart_service` action is intentionally not implemented yet and is safely blocked by the executor.

## 5. Safety Policy

The self-healing executor follows these restrictions:

* Only predefined actions are allowed.
* Arbitrary shell commands cannot be supplied by the user.
* Arbitrary filesystem paths cannot be supplied by the healing recommendation.
* `clear_cache` operates only on the current user's cache directory.
* The cache directory is resolved before execution.
* The resolved execution target must exactly match the approved `~/.cache` directory.
* Cache cleanup cannot be redirected to another filesystem location.
* The cache directory itself is not deleted.
* Symbolic links are not followed as directories.
* No `sudo` or elevated privileges are used.
* Human approval is required before execution.
* Unsupported actions are rejected.
* Unimplemented service restart operations are rejected safely.

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

The implementation reports the number of items removed and raises an error if the cleanup partially fails.

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

If the completed operation takes longer than the configured threshold, the executor raises a controlled `TimeoutError`.

This implementation is a **post-execution duration check**. It does not forcibly terminate a filesystem operation while it is running.

This approach avoids unsafe termination of an active filesystem operation while still providing measurable execution-duration monitoring and controlled timeout reporting.

## 8. Healing Audit Log

Every healing decision and execution attempt is recorded in SQLite.

The `healing_audit_logs` table stores:

* timestamp
* metric
* action
* approval status
* execution status
* result
* error information
* record creation time

This provides traceability for human decisions and system actions.

## 9. Real Linux Execution Test

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

## 10. Audit Verification

The SQLite audit log confirmed the execution history.

Example records:

```text
disk_percent | clear_cache     | approved | success       | 21 items removed
disk_percent | clear_cache     | approved | success       | 0 items removed
cpu_percent  | restart_service | approved | failed        | Healing action execution failed
cpu_percent  | restart_service | rejected | not_executed  | Healing action rejected by human operator
```

These records demonstrate that the system can distinguish between:

* successful healing,
* failed execution,
* rejected actions, and
* actions that were not executed.

## 11. Testing

The self-healing executor and workflow are covered by automated tests.

The executor tests verify:

* approved actions can execute,
* unapproved actions are blocked,
* unknown actions are blocked,
* arbitrary commands are blocked,
* service restart is safely rejected because it is not implemented,
* the execution-duration threshold is configured,
* cache cleanup removes test data,
* unsafe cache targets are rejected.

The workflow tests verify:

* approved actions execute successfully,
* successful execution is audited,
* rejected actions are audited as `not_executed`,
* unapproved execution attempts are audited as failed.

The complete project test suite currently passes:

```text
51 passed
```

## 12. Current Implementation Status

| Component                      | Status             |
| ------------------------------ | ------------------ |
| Human approval                 | Implemented        |
| Action mapping                 | Implemented        |
| Healing executor               | Implemented        |
| Real `clear_cache`             | Implemented        |
| Audit logging                  | Implemented        |
| Execution success tracking     | Implemented        |
| Execution failure tracking     | Implemented        |
| Rejection tracking             | Implemented        |
| Strict cache target validation | Implemented        |
| Execution duration monitoring  | Implemented        |
| Real Linux execution test      | Completed          |
| `restart_service`              | Not implemented    |
| Multiple healing actions       | Future enhancement |

## 13. Future Improvements

Future versions can add additional controlled healing actions such as:

* safe service restart,
* temporary-file cleanup,
* resource-aware process management,
* configurable safety policies,
* stronger rollback mechanisms,
* multi-server healing support.

All future actions should preserve the project's human-approval and safety-first design.
