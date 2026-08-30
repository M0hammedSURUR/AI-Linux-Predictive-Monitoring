# Prediction Design

## 1. Purpose

The prediction layer estimates whether important Linux system
metrics are moving toward potentially abnormal levels.

It provides an early warning mechanism before a threshold is
actually exceeded.

## 2. Input

The prediction component receives processed telemetry records
from the preprocessing layer.

The current implementation uses:

- CPU usage
- Memory usage
- Disk usage

## 3. Prediction Method

The initial implementation uses a simple trend-based method.

The change between the two most recent observations is calculated:

predicted_value = current_value + (current_value - previous_value)

This provides a simple and explainable estimate of the next metric value.

## 4. Prediction Thresholds

| Metric | Threshold |
|---|---:|
| CPU usage | 80% |
| Memory usage | 80% |
| Disk usage | 90% |

## 5. Risk Levels

### Low

The predicted value remains comfortably below the threshold.

### Medium

The predicted value reaches at least 80% of the configured threshold.

### High

The predicted value reaches or exceeds the configured threshold.

## 6. Output

Each prediction produces a `PredictionResult` containing:

- Timestamp
- Metric name
- Current value
- Predicted value
- Threshold
- Risk level
- Human-readable message

## 7. Current Architecture

```text
Linux System
     |
     v
Telemetry Collector
     |
     v
SQLite Database
     |
     v
Preprocessing
     |
     v
Telemetry Predictor
     |
     v
Prediction Result
     |
     v
Future Dashboard / Alerting / Self-Healing
