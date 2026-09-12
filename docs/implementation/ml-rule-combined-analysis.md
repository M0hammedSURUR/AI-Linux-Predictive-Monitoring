# ML and Rule-Based Combined Anomaly Analysis

## 1. Overview

LinuxSentinel AI uses two complementary anomaly detection approaches:

1. Rule-based anomaly detection
2. Machine learning-based anomaly detection

The rule-based detector identifies known abnormal conditions using configured system thresholds. The ML detector uses Isolation Forest to identify unusual telemetry patterns.

A combined analysis layer evaluates both signals without allowing the ML model to directly trigger self-healing actions.

---

## 2. Detection Architecture

The combined anomaly detection architecture follows this flow:

    Telemetry
        |
        +-----------------------+
        |                       |
        v                       v
    Rule-Based Detector     ML Detector
        |                       |
        +-----------+-----------+
                    |
                    v
            Combined Analysis
                    |
                    v
              Recommendation
                    |
                    v
              Human Approval
                    |
                    v
               Self-Healing

The rule-based detector remains the primary mechanism for known threshold violations. The ML detector provides an additional experimental signal.

---

## 3. Rule-Based Detection

The rule-based detector monitors:

- CPU usage
- Memory usage
- Disk usage
- 1-minute system load

Configured thresholds determine whether a metric is considered anomalous.

Severity is calculated based on the amount by which the observed value exceeds the configured threshold:

| Condition | Severity |
|---|---|
| Threshold exceeded | Medium |
| 1.10 × threshold or higher | High |
| 1.25 × threshold or higher | Critical |

Each detected anomaly contains:

- Timestamp
- Metric
- Observed value
- Threshold
- Severity
- Explanation

---

## 4. Machine Learning Detection

The ML detector uses the Isolation Forest algorithm from scikit-learn.

The current feature set contains:

- CPU percentage
- Memory percentage
- Disk percentage
- 1-minute system load

The detector requires at least 10 telemetry records for training.

The model is configured with:

- Contamination: `0.23`
- Random state: `42`

The ML detector identifies unusual patterns rather than checking fixed thresholds.

ML results are treated as experimental signals and are not directly connected to the self-healing executor.

---

## 5. Combined Analysis

The `CombinedAnomalyDetector` combines the results from both detection mechanisms.

Four analysis states are supported.

### High Confidence

Both rule-based and ML detection identify an anomaly.

    Rule anomaly = True
    ML anomaly   = True
    Confidence   = High

This represents stronger evidence because both detection approaches agree.

### Medium Confidence

Only the rule-based detector identifies an anomaly.

    Rule anomaly = True
    ML anomaly   = False
    Confidence   = Medium

This represents a known threshold violation without ML confirmation.

### Experimental

Only the ML detector identifies an anomaly.

    Rule anomaly = False
    ML anomaly   = True
    Confidence   = Experimental

This signal is intentionally not treated as sufficient evidence for automated self-healing.

### Normal

Neither detector identifies an anomaly.

    Rule anomaly = False
    ML anomaly   = False
    Confidence   = Normal

---

## 6. Safety Boundary

The ML detector cannot directly execute a healing action.

The intended control flow is:

    ML Signal
       |
       v
    Combined Analysis
       |
       v
    Recommendation
       |
       v
    Human Approval
       |
       v
    Self-Healing Workflow
       |
       v
    Approved Safe Action

This preserves the human-in-the-loop safety requirement of LinuxSentinel AI.

Only predefined and validated self-healing actions can reach the execution stage.

The ML detector does not bypass:

- Recommendation generation
- Human approval
- Self-healing safety validation
- Approved action execution

This separation prevents experimental ML predictions from directly modifying the Linux system.

---

## 7. Dashboard Integration

The Streamlit dashboard now displays:

- Rule-based anomaly status
- Experimental ML anomaly count
- Experimental ML signals
- Combined confidence classification
- Explanations for detected conditions

The existing recommendation and self-healing workflow remains separate from the experimental ML signal.

This prevents an ML false positive from directly causing a system-changing operation.

The dashboard clearly distinguishes between:

- Known threshold-based anomalies
- Experimental ML-only signals
- Combined high-confidence anomalies
- Normal system conditions

---

## 8. Testing

Dedicated tests were added for the combined analysis layer.

The following cases are tested:

1. Rule-based and ML agreement
2. Rule-based anomaly only
3. ML anomaly only
4. Normal telemetry

All four combined-detector tests passed.

The complete project test suite also passed:

    60 passed

This confirms that the combined anomaly analysis and dashboard integration did not break the existing:

- Collector
- Database
- Preprocessing
- Prediction
- Recommendation
- Self-healing

components.

---

## 9. Controlled ML Evaluation

The ML detector was previously evaluated using a controlled synthetic dataset containing:

- 100 normal records
- 30 anomaly records
- 130 total records

The evaluation produced:

- Accuracy: 92.31%
- Precision: 83.33%
- Recall: 83.33%
- F1 score: 83.33%

These values represent a controlled experiment on generated data and should not be interpreted as production accuracy.

The evaluation was performed using a deterministic synthetic dataset so that the ML anomaly detection approach could be tested under controlled conditions.

The results demonstrate that the Isolation Forest model can identify abnormal telemetry patterns in the experimental dataset.

---

## 10. Relationship Between Rule-Based and ML Detection

The two detection mechanisms serve different purposes.

### Rule-Based Detection

Rule-based detection is deterministic and threshold-driven.

It is suitable for:

- Known resource limits
- Clearly defined system conditions
- Explainable anomaly detection
- Safety-critical monitoring decisions

### ML Detection

ML detection is pattern-based and experimental.

It is suitable for:

- Identifying unusual telemetry combinations
- Detecting patterns that may not exceed individual thresholds
- Supporting additional anomaly analysis
- Future improvement of predictive monitoring

The ML detector therefore complements the rule-based detector rather than replacing it.

---

## 11. Human-in-the-Loop Design

LinuxSentinel AI follows a human-approved self-healing approach.

The anomaly detection layer can identify suspicious conditions and the recommendation layer can suggest appropriate actions.

However, the system does not allow an anomaly detector to directly execute a healing action.

The intended workflow is:

    Telemetry
       |
       v
    Anomaly Detection
       |
       v
    Combined Analysis
       |
       v
    Recommendation
       |
       v
    Human Approval
       |
       v
    Safety Validation
       |
       v
    Self-Healing Action
       |
       v
    Audit Logging

This design improves system safety and accountability.

---

## 12. Conclusion

The combined anomaly architecture provides two complementary detection mechanisms while maintaining a safe human-approved self-healing workflow.

Rule-based detection provides deterministic monitoring of known conditions, while Isolation Forest provides an experimental mechanism for identifying unusual telemetry patterns.

The combined analysis layer evaluates the two signals and classifies the result as:

- Normal
- Medium confidence
- High confidence
- Experimental

The architecture improves anomaly analysis without allowing experimental ML predictions to bypass human approval or the existing self-healing safety controls.

This provides a safe foundation for future improvements to LinuxSentinel AI's predictive monitoring and anomaly detection capabilities.
