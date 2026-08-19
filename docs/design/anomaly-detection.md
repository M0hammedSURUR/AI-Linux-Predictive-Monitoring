# Anomaly Detection Design

## 1. Purpose

The anomaly detection module identifies abnormal Linux system conditions from processed telemetry data.

It provides the first intelligence layer of the monitoring platform and prepares the system for future predictive analysis and human-approved self-healing.

## 2. Detection Approach

The initial implementation uses threshold-based rule detection.

The following metrics are monitored:

| Metric | Default Threshold |
|---|---:|
| CPU utilization | 80% |
| Memory utilization | 80% |
| Disk utilization | 90% |
| 1-minute system load | 4.0 |

## 3. Detection Process

Processed telemetry is passed to the `AnomalyDetector`.

Each metric is compared against its configured threshold.

If one or more thresholds are exceeded, the record is classified as anomalous.

The detector also records the reasons for the anomaly.

## 4. Anomaly Result

Each detection produces an `AnomalyResult` containing:

- timestamp
- anomaly status
- list of detected reasons

## 5. Validation

The detector was tested using both normal and artificially abnormal telemetry.

Normal telemetry produced:

`Anomaly detected: False`

Artificial telemetry containing high CPU, memory, disk, and load values produced:

`Anomaly detected: True`

Detected reasons:

- High CPU usage
- High memory usage
- High disk usage
- High system load

## 6. Current Limitation

The current implementation uses static thresholds.

Future versions may incorporate statistical methods and machine-learning models to identify unusual behavior based on historical telemetry patterns.

## 7. Future Integration

The anomaly detection module will later provide input to:

- predictive analysis
- recommendation generation
- human approval workflows
- self-healing actions
- audit logging
