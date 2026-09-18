# End-to-End Pipeline Integration

## 1. Overview

Day 27 integrates the major components of the LinuxSentinel AI platform into a complete monitoring-to-healing workflow.

The integrated pipeline is:

Telemetry Collection → Preprocessing → Anomaly Detection → Prediction → Recommendation → Human Approval → Self-Healing → Audit

The purpose of this integration is to verify that the independently developed components can work together as a single system workflow.

---

## 2. Integrated Components

The following project components participate in the workflow:

1. Telemetry Collector
2. Telemetry Preprocessor
3. Rule-Based Anomaly Detector
4. ML Anomaly Detector
5. Prediction Engine
6. Recommendation Engine
7. Self-Healing Workflow
8. Self-Healing Executor
9. Healing Audit Repository

---

## 3. Pipeline Flow

### 3.1 Telemetry

The monitoring system collects Linux system telemetry such as:

- CPU usage
- Memory usage
- Disk usage
- System load
- Process count
- Disk I/O
- Network I/O

The telemetry is stored in SQLite.

### 3.2 Preprocessing

Stored telemetry is converted into analysis-ready `ProcessedTelemetry` records.

The preprocessing stage also calculates rate-based features such as:

- Disk read rate
- Disk write rate
- Network send rate
- Network receive rate

### 3.3 Anomaly Detection

The rule-based anomaly detector checks configured thresholds for:

- CPU usage
- Memory usage
- Disk usage
- System load

The ML anomaly detector provides an additional experimental signal using Isolation Forest.

### 3.4 Prediction

The prediction engine uses recent telemetry history and a rolling linear trend to estimate future resource usage.

Predictions are classified into:

- Low risk
- Medium risk
- High risk

### 3.5 Recommendation

The recommendation engine converts detected anomalies and high-risk predictions into human-readable recommendations.

Each recommendation contains:

- Metric
- Severity
- Description
- Suggested action

### 3.6 Human Approval

Recommendations are converted into predefined healing actions.

Healing actions initially have a `pending` status.

The operator must explicitly approve or reject the action.

No healing action is executed automatically.

### 3.7 Self-Healing

After explicit human approval, the approved action can be executed by the self-healing executor.

Only predefined and safety-checked actions are permitted.

The currently implemented executable healing action is:

- `clear_cache`

### 3.8 Audit

The result of the healing operation is recorded in the healing audit log.

The audit records include:

- Timestamp
- Metric
- Action
- Approval status
- Execution status
- Result
- Error information

---

## 4. Integration Test

A dedicated integration test was created:

    tests/test_pipeline_integration.py

The test verifies the complete path from anomaly detection through human-approved healing.

The test uses deterministic telemetry containing a high disk-usage condition.

The detected disk anomaly generates a recommendation.

The recommendation is mapped to the safe `clear_cache` action.

The action begins in the `pending` state.

The test then simulates explicit human approval.

The approved action is executed.

Finally, the test verifies that the execution succeeds and that the audit result records the approved status and successful execution.

---

## 5. Integration Test Result

The dedicated integration test passed successfully:

    1 passed in 0.40s

The complete project test suite also passed:

    69 passed in 3.00s

This confirms that the new integration test did not introduce regressions into the existing components.

---

## 6. Human Approval Safety

The integration maintains the project's human-in-the-loop safety requirement.

The workflow is:

    Recommendation
          ↓
    Pending Action
          ↓
    Human Approval
          ↓
    Approved Action
          ↓
    Safe Execution
          ↓
    Audit Log

An action cannot be executed while it remains pending.

This prevents the monitoring system from directly converting an anomaly into an autonomous system modification.

---

## 7. Implementation

The main workflow components are implemented in:

    src/preprocessing/telemetry_preprocessor.py
    src/anomaly_detection/detector.py
    src/anomaly_detection/ml_detector.py
    src/prediction/predictor.py
    src/recommendations/engine.py
    src/self_healing/workflow.py
    src/self_healing/executor.py
    src/self_healing/audit_repository.py

The integration test is implemented in:

    tests/test_pipeline_integration.py

---

## 8. Limitations

The current integration test uses deterministic synthetic telemetry rather than continuously collected production telemetry.

The integration currently verifies the safe `clear_cache` healing path.

The `restart_service` action remains intentionally restricted because safe service restart handling requires additional service-management controls.

The ML anomaly detector remains experimental and does not directly trigger healing actions.

---

## 9. Conclusion

Day 27 successfully integrates the major LinuxSentinel AI components into a tested end-to-end workflow.

The system can now demonstrate the complete logical pipeline from system telemetry and anomaly detection through prediction, recommendation, human approval, safe healing execution, and audit logging.

The complete test suite passes with 69 tests, providing evidence that the integrated workflow works without breaking existing functionality.
