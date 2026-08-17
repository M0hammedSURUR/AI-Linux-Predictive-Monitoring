# Telemetry Collector

## Purpose

The telemetry collector is responsible for obtaining system-level
performance information directly from the Linux operating system.

## Initial Metrics

The first implementation collects:

- CPU utilization
- Memory utilization
- Swap utilization
- Root filesystem utilization
- One-minute system load
- Timestamp

## Technology

Python and psutil are used for the initial implementation.

## Design

The collector is separated from data processing and machine-learning
components so that telemetry collection can be independently tested.

## Timestamp Handling

Telemetry timestamps are stored as timezone-aware UTC timestamps.

## Current Limitations

The initial implementation does not yet collect:

- network traffic
- disk I/O
- process-level metrics
- service state
- system logs

These will be added incrementally in subsequent development iterations.

## Testing

Unit tests verify:

- TelemetryRecord creation
- Collector output type
- Validity of collected metric ranges

## Continuous Collection Experiment

A continuous telemetry collection experiment was performed on the Linux Mint development system.

### Configuration

- Collection interval: 5 seconds
- Collection duration: approximately 177 seconds
- Telemetry samples collected: 35
- Storage: SQLite
- Database: `data/monitoring.db`

### Observed Results

| Metric | Result |
|---|---:|
| Samples | 35 |
| First sample | 2026-08-17T09:11:59.515495+00:00 |
| Last sample | 2026-08-17T09:14:56.497275+00:00 |
| CPU range | 0.0–2.4% |
| Memory range | 25.7–27.8% |
| Process count range | 295–300 |
| Database size | 24 KB |

The effective sampling interval was approximately 5.21 seconds per sample. The difference from the configured 5-second interval is caused by the execution time required to collect and store each telemetry record before the sleep interval begins.

### Initial Observation

The experiment successfully demonstrated continuous collection and persistence of real Linux telemetry into SQLite without runtime errors.

The measured database size indicates that SQLite is suitable for the initial single-machine implementation. A larger dataset will be collected later for preprocessing and machine-learning experiments.

### Engineering Decision

The 5-second interval is currently treated as an initial experimental configuration rather than a final system requirement. Further experiments will determine the appropriate collection and aggregation intervals for anomaly detection and predictive analysis.

