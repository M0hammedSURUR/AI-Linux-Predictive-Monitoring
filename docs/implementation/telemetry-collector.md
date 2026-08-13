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
