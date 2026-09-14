# Test Case Specification

## 1. Purpose

This document defines the automated test cases used to verify the functional components of the AI-Powered Linux Predictive Monitoring & Human-Approved Self-Healing Platform.

The test cases are based on the implemented system components and correspond to the automated tests in the `tests/` directory.

## 2. Test Environment

| Item              | Configuration                                                          |
| ----------------- | ---------------------------------------------------------------------- |
| Operating System  | Linux Mint 22.3 Cinnamon                                               |
| Python            | 3.12.3                                                                 |
| Testing Framework | pytest 9.1.1                                                           |
| Test Type         | Automated unit, component, repository, safety, and integration testing |

## 3. Test Case Categories

The automated test suite covers:

1. Telemetry collection
2. Database operations
3. Telemetry preprocessing
4. Anomaly detection
5. Machine-learning anomaly detection
6. Prediction
7. Recommendation generation
8. Self-healing action mapping
9. Self-healing approval and rejection
10. Self-healing safety
11. Self-healing execution
12. Audit logging
13. End-to-end pipeline integration

## 4. Test Cases

### 4.1 Telemetry Collection

| Test ID | Automated Test                                   | Purpose                                                 |
| ------- | ------------------------------------------------ | ------------------------------------------------------- |
| TC-001  | `test_telemetry_record_creation`                 | Verify telemetry records can be created correctly.      |
| TC-002  | `test_system_collector_returns_telemetry_record` | Verify the system collector returns a telemetry record. |
| TC-003  | `test_system_collector_values_are_valid`         | Verify collected telemetry values are valid.            |

### 4.2 Database Operations

| Test ID | Automated Test                           | Purpose                                                 |
| ------- | ---------------------------------------- | ------------------------------------------------------- |
| TC-004  | `test_database_initialization`           | Verify database initialization succeeds.                |
| TC-005  | `test_telemetry_record_can_be_saved`     | Verify telemetry records can be stored in the database. |
| TC-006  | `test_prediction_can_be_saved`           | Verify prediction records can be stored.                |
| TC-007  | `test_anomaly_event_creation`            | Verify anomaly events can be created.                   |
| TC-008  | `test_anomaly_event_can_be_saved`        | Verify anomaly events can be stored.                    |
| TC-009  | `test_audit_log_can_be_saved_and_loaded` | Verify audit records can be stored and retrieved.       |

### 4.3 Telemetry Preprocessing

| Test ID | Automated Test                                 | Purpose                                                                |
| ------- | ---------------------------------------------- | ---------------------------------------------------------------------- |
| TC-010  | `test_preprocessor_returns_processed_records`  | Verify raw telemetry is converted into processed records.              |
| TC-011  | `test_processed_records_contain_derived_rates` | Verify disk and network rates are calculated.                          |
| TC-012  | `test_processed_records_preserve_core_metrics` | Verify important telemetry metrics are preserved during preprocessing. |

### 4.4 Rule-Based Anomaly Detection

| Test ID | Automated Test                         | Purpose                                                    |
| ------- | -------------------------------------- | ---------------------------------------------------------- |
| TC-013  | `test_normal_record_has_no_anomalies`  | Verify normal telemetry does not produce anomalies.        |
| TC-014  | `test_high_cpu_is_detected`            | Verify high CPU usage is detected.                         |
| TC-015  | `test_critical_severity_is_detected`   | Verify critical anomaly severity is assigned correctly.    |
| TC-016  | `test_high_severity_is_detected`       | Verify high anomaly severity is assigned correctly.        |
| TC-017  | `test_medium_severity_is_detected`     | Verify medium anomaly severity is assigned correctly.      |
| TC-018  | `test_multiple_anomalies_are_detected` | Verify multiple abnormal metrics can be detected together. |

### 4.5 Machine-Learning Anomaly Detection

| Test ID | Automated Test                                 | Purpose                                                                    |
| ------- | ---------------------------------------------- | -------------------------------------------------------------------------- |
| TC-019  | `test_isolation_forest_can_detect_an_outlier`  | Verify the Isolation Forest model can identify an outlier.                 |
| TC-020  | `test_ml_detector_detects_anomalous_pattern`   | Verify the ML anomaly detector identifies an unusual pattern.              |
| TC-021  | `test_isolation_forest_evaluation_metrics`     | Verify ML anomaly detection evaluation metrics are calculated.             |
| TC-022  | `test_combined_detector_normal`                | Verify combined detection reports normal conditions correctly.             |
| TC-023  | `test_combined_detector_rule_only`             | Verify combined detection handles rule-only anomalies.                     |
| TC-024  | `test_combined_detector_ml_only`               | Verify combined detection handles ML-only anomalies.                       |
| TC-025  | `test_combined_detector_rule_and_ml_agreement` | Verify agreement between rule-based and ML detection is handled correctly. |

### 4.6 Predictive Monitoring

| Test ID | Automated Test                                     | Purpose                                                   |
| ------- | -------------------------------------------------- | --------------------------------------------------------- |
| TC-026  | `test_cpu_prediction_is_generated`                 | Verify CPU risk prediction is generated.                  |
| TC-027  | `test_high_cpu_prediction_is_detected`             | Verify high-risk CPU prediction is identified.            |
| TC-028  | `test_predictor_requires_two_records`              | Verify prediction requires sufficient historical records. |
| TC-029  | `test_predictor_uses_recent_history`               | Verify recent telemetry history is used for prediction.   |
| TC-030  | `test_prediction_evaluation_returns_valid_metrics` | Verify prediction evaluation produces valid metrics.      |

### 4.7 Recommendation Generation

| Test ID | Automated Test                                         | Purpose                                                                  |
| ------- | ------------------------------------------------------ | ------------------------------------------------------------------------ |
| TC-031  | `test_high_cpu_anomaly_generates_recommendation`       | Verify high CPU anomalies generate recommendations.                      |
| TC-032  | `test_high_memory_anomaly_generates_recommendation`    | Verify high memory anomalies generate recommendations.                   |
| TC-033  | `test_high_disk_anomaly_generates_recommendation`      | Verify high disk anomalies generate recommendations.                     |
| TC-034  | `test_high_load_anomaly_generates_recommendation`      | Verify high system load generates recommendations.                       |
| TC-035  | `test_high_risk_prediction_generates_recommendation`   | Verify high-risk predictions generate recommendations.                   |
| TC-036  | `test_low_risk_prediction_generates_no_recommendation` | Verify low-risk predictions do not generate unnecessary recommendations. |
| TC-037  | `test_normal_condition_generates_no_recommendation`    | Verify normal conditions do not generate recommendations.                |

### 4.8 Self-Healing Action Mapping

| Test ID | Automated Test                                       | Purpose                                                                     |
| ------- | ---------------------------------------------------- | --------------------------------------------------------------------------- |
| TC-038  | `test_cpu_recommendation_maps_to_restart_service`    | Verify CPU recommendations map to the predefined service-restart action.    |
| TC-039  | `test_memory_recommendation_maps_to_restart_service` | Verify memory recommendations map to the predefined service-restart action. |
| TC-040  | `test_disk_recommendation_maps_to_clear_cache`       | Verify disk recommendations map to the predefined cache-cleanup action.     |
| TC-041  | `test_unknown_metric_has_no_healing_action`          | Verify unsupported metrics do not create healing actions.                   |

### 4.9 Self-Healing Approval Workflow

| Test ID | Automated Test                                       | Purpose                                                     |
| ------- | ---------------------------------------------------- | ----------------------------------------------------------- |
| TC-042  | `test_pending_action_can_be_approved`                | Verify a pending healing action can be approved.            |
| TC-043  | `test_pending_action_can_be_rejected`                | Verify a pending healing action can be rejected.            |
| TC-044  | `test_approved_action_cannot_be_approved_again`      | Verify an already approved action cannot be approved again. |
| TC-045  | `test_rejected_action_cannot_be_rejected_again`      | Verify an already rejected action cannot be rejected again. |
| TC-046  | `test_recommendation_creates_pending_healing_action` | Verify recommendations create pending healing actions.      |
| TC-047  | `test_high_risk_prediction_creates_healing_action`   | Verify high-risk predictions can create healing actions.    |
| TC-048  | `test_unknown_metric_does_not_create_action`         | Verify unsupported metrics do not create healing actions.   |

### 4.10 Self-Healing Safety

| Test ID | Automated Test                                 | Purpose                                                                         |
| ------- | ---------------------------------------------- | ------------------------------------------------------------------------------- |
| TC-049  | `test_unapproved_action_cannot_be_executed`    | Verify unapproved actions cannot be executed.                                   |
| TC-050  | `test_unknown_action_is_blocked`               | Verify unknown healing actions are blocked.                                     |
| TC-051  | `test_arbitrary_command_is_blocked`            | Verify arbitrary command execution is blocked.                                  |
| TC-052  | `test_cache_cleanup_rejects_unsafe_target`     | Verify unsafe cache targets are rejected.                                       |
| TC-053  | `test_real_service_restart_is_not_implemented` | Verify real service restart is not executed through the current implementation. |
| TC-054  | `test_execution_timeout_is_configured`         | Verify execution timeout configuration is present.                              |

### 4.11 Self-Healing Execution

| Test ID | Automated Test                                          | Purpose                                                         |
| ------- | ------------------------------------------------------- | --------------------------------------------------------------- |
| TC-055  | `test_approved_allowed_action_is_executed`              | Verify an approved predefined action can be executed.           |
| TC-056  | `test_approved_action_executes_and_is_audited`          | Verify successful execution is recorded in the audit system.    |
| TC-057  | `test_rejected_action_is_audited`                       | Verify rejected actions are recorded as not executed.           |
| TC-058  | `test_unapproved_action_execution_is_audited_as_failed` | Verify an attempted unapproved execution is recorded as failed. |

### 4.12 Self-Healing Audit Logging

| Test ID | Automated Test                      | Purpose                                                       |
| ------- | ----------------------------------- | ------------------------------------------------------------- |
| TC-059  | `test_successful_healing_audit_log` | Verify successful healing execution produces an audit record. |
| TC-060  | `test_failed_healing_audit_log`     | Verify failed healing execution produces an audit record.     |

### 4.13 End-to-End Integration

| Test ID | Automated Test                                 | Purpose                                                                                                           |
| ------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| TC-061  | `test_complete_monitoring_to_healing_pipeline` | Verify the complete monitoring-to-healing workflow from anomaly detection through approval, execution, and audit. |

## 5. Additional Test Coverage

The automated test suite also includes repository and component-level verification for prediction, anomaly, telemetry, and audit data persistence.

All implemented tests are executed together using pytest.

## 6. Test Execution Command

The complete test suite is executed using:

```bash
pytest -q
```

## 7. Expected Result

The expected result is that all implemented automated tests pass without failures.

The current verified execution result is:

```text
63 passed
```

## 8. Requirement Traceability

The test cases support verification of the implemented functional requirements identified in the Requirements Traceability Matrix.

Requirements that are currently not implemented remain explicitly marked as such rather than being represented by unsupported test cases.

## 9. Conclusion

The test case specification provides a structured mapping between implemented system functionality and the automated tests used to verify it.

The current project contains 63 automated tests covering the implemented monitoring, preprocessing, anomaly detection, prediction, recommendation, self-healing, safety, audit, and integration functionality.
