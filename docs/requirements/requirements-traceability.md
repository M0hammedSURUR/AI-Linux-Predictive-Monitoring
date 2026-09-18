# Requirements Traceability Matrix

This matrix maps functional requirements to their related use cases and current implementation/test evidence.

| Requirement | Description | Use Case | Implementation / Test Evidence | Status |
| ----------- | ----------- | -------- | ------------------------------ | ------ |
| FR-01 | Collect Linux system telemetry at configurable intervals | UC-01 | `src/collector/` and collector tests | Implemented |
| FR-02 | Collect CPU utilization data | UC-01 | `SystemCollector` and telemetry model tests | Implemented |
| FR-03 | Collect memory and swap utilization data | UC-01 | `SystemCollector` and telemetry model tests | Implemented |
| FR-04 | Collect disk usage and disk I/O information | UC-01 | `SystemCollector` and telemetry model tests | Implemented |
| FR-05 | Collect network activity information | UC-01 | `SystemCollector` and telemetry model tests | Implemented |
| FR-06 | Collect process-level resource information | UC-01 | Process information in telemetry collector/model | Implemented |
| FR-07 | Monitor selected Linux services | UC-02 | `src/service_monitor/`, `SystemdServiceMonitor`, service-monitoring tests | Implemented |
| FR-08 | Collect selected relevant system/application log information | UC-02 | `src/log_monitor/`, `JournalMonitor`, log-monitoring tests | Implemented |
| FR-09 | Store timestamped telemetry data for historical analysis | UC-02 | SQLite database, `TelemetryRepository`, and database tests | Implemented |
| FR-10 | Preprocess collected telemetry for analysis | UC-02 | `TelemetryPreprocessor` and preprocessing tests | Implemented |
| FR-11 | Detect abnormal system behavior | UC-03 | Rule-based anomaly detector, ML detector, combined detector, and tests | Implemented |
| FR-12 | Calculate selected system-risk predictions | UC-04 | `Predictor` and prediction tests | Implemented |
| FR-13 | Provide information about factors contributing to detected risks | UC-05 | Anomaly explanations, recommendation descriptions, and prediction messages | Implemented |
| FR-14 | Calculate an understandable system health/risk status | UC-04/05 | Dashboard Overall System Health section and live full-system test | Implemented |
| FR-15 | Generate predefined maintenance recommendations | UC-06 | `RecommendationEngine` and recommendation tests | Implemented |
| FR-16 | Require administrator approval before executing corrective action | UC-07/08 | `SelfHealingEngine`, workflow, and safety tests | Implemented |
| FR-17 | Execute only predefined and authorized corrective actions | UC-09 | `HealingActionMapper`, executor, and safety tests | Implemented |
| FR-18 | Support dry-run or simulation mode for corrective actions | UC-11 | Dashboard self-healing simulation mode and live full-system test | Implemented |
| FR-19 | Record recommendations, approvals, rejections, executions and results in an audit log | UC-10 | `HealingAuditRepository`, audit database, audit tests, and live verification | Implemented |
| FR-20 | Provide a dashboard for current and historical system information | UC-01/02/04 | Streamlit dashboard and live full-system test | Implemented |

## Test Suite Evidence

The current automated test suite contains **69 tests**, with all tests passing.

```text
69 passed in 3.00s

The test suite covers telemetry collection, database operations, preprocessing, anomaly detection, prediction, recommendations, self-healing safety, audit logging, service monitoring, log monitoring, ML evaluation, and end-to-end pipeline integration.

Traceability Status
Implemented requirements: 20
Not yet implemented requirements: 0
Total functional requirements: 20

All functional requirements in the current requirements baseline have corresponding implementation and/or test evidence.

The traceability matrix is maintained to connect the original requirements with their implementation, automated tests, and live-system verification evidence.
