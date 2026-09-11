# Anomaly Detection Implementation

## 1. Overview

The anomaly detection component identifies abnormal Linux system conditions from collected telemetry.

The current implementation provides a rule-based baseline using configurable thresholds for CPU usage, memory usage, disk usage, and system load.

The anomaly detection result is designed to integrate with the recommendation and self-healing components.

## 2. Detection Metrics

The detector currently evaluates:

* `cpu_percent` — CPU utilization percentage
* `memory_percent` — memory utilization percentage
* `disk_percent` — disk utilization percentage
* `load_1m` — one-minute system load

Default thresholds are:

| Metric       | Threshold |
| ------------ | --------: |
| CPU usage    |       80% |
| Memory usage |       80% |
| Disk usage   |       90% |
| System load  |       4.0 |

A metric is considered anomalous when its observed value is greater than or equal to its configured threshold.

## 3. Anomaly Result Model

Each detected anomalous metric produces an `AnomalyResult`.

The result contains:

* Timestamp
* Anomaly status
* Metric name
* Observed value
* Configured threshold
* Severity
* Explanation

This structure provides the recommendation engine and dashboard with a consistent representation of anomaly information.

## 4. Severity Classification

The detector assigns severity according to the amount by which the observed value exceeds its threshold.

| Condition                         | Severity |
| --------------------------------- | -------- |
| Observed value ≥ threshold × 1.25 | Critical |
| Observed value ≥ threshold × 1.10 | High     |
| Observed value ≥ threshold        | Medium   |

For example, with a CPU threshold of 80%:

* 85% → Medium
* 95% → High
* 100% → Critical

## 5. Multiple Anomalies

The detector returns one `AnomalyResult` for each anomalous metric.

For example, if CPU, memory, disk, and system load all exceed their thresholds, four separate anomaly results are generated.

This allows each anomaly to be handled independently by later recommendation and self-healing stages.

## 6. Dashboard Integration

The dashboard processes the anomaly results and displays active anomalies with:

* Timestamp
* Metric
* Observed value
* Threshold
* Severity
* Explanation

Normal telemetry produces no active anomaly entries.

The dashboard was updated to handle the detector's list-based result structure correctly.

## 7. Testing

The anomaly detection implementation is covered by automated tests for:

* Normal telemetry with no anomalies
* High CPU detection
* Multiple simultaneous anomalies
* Critical severity
* Medium severity

The Day 19 anomaly detection test suite contains **5 tests**, all of which pass.

The complete project test suite currently contains **53 passing tests**.

## 8. Current Limitation and Future AI Enhancement

The current detector is a deterministic threshold-based baseline.

It does not yet learn normal system behavior from historical telemetry.

A future implementation can introduce machine-learning-based anomaly detection using historical system metrics and learned normal operating patterns.

The threshold-based detector provides a safe and explainable baseline before introducing learned anomaly detection.
