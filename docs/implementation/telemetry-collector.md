# Telemetry Collector

## 1. Purpose

The telemetry collector obtains system-level performance information directly from the Linux operating system.

It collects real-time telemetry using Python and the `psutil` library and provides structured records for storage, preprocessing, anomaly detection, prediction, and dashboard monitoring.

## 2. Technology

- **Programming language:** Python
- **System monitoring library:** psutil
- **Data model:** Python dataclass
- **Timestamp:** Python datetime with UTC timezone
- **Storage integration:** SQLite

## 3. Collected Metrics

The current implementation collects the following metrics:

### CPU and Memory

- CPU utilization (`cpu_percent`)
- Memory utilization (`memory_percent`)
- Swap utilization (`swap_percent`)

### Disk and System Load

- Root filesystem utilization (`disk_percent`)
- One-minute system load (`load_1m`)
- Cumulative disk read bytes (`disk_read_bytes`)
- Cumulative disk write bytes (`disk_write_bytes`)

### Network

- Cumulative network bytes sent (`network_bytes_sent`)
- Cumulative network bytes received (`network_bytes_received`)

### Process Monitoring

- Total process count (`process_count`)
- Name of the top CPU-consuming process (`top_cpu_process`)
- Name of the top memory-consuming process (`top_memory_process`)

### Timestamp

- Time of collection, stored as a timezone-aware UTC timestamp (`timestamp`).

## 4. Implementation Design

The collector is implemented using two main components.

### 4.1 TelemetryRecord

The `TelemetryRecord` dataclass in `src/collector/models.py` defines the structure of one telemetry snapshot.

It provides a consistent data structure containing all collected metrics.

### 4.2 SystemCollector

The `SystemCollector` class in `src/collector/system_collector.py` collects system information using `psutil`.

Its `collect()` method:

1. Reads CPU utilization.
2. Retrieves memory and swap usage.
3. Reads root filesystem utilization.
4. Retrieves cumulative disk I/O counters.
5. Retrieves cumulative network I/O counters.
6. Enumerates running processes.
7. Determines the top CPU-consuming and memory-consuming process names.
8. Retrieves the one-minute system load.
9. Creates and returns a `TelemetryRecord`.

The `_top_process()` helper handles processes that disappear or cannot be accessed during collection.

## 5. Timestamp Handling

Each telemetry record receives a timezone-aware UTC timestamp using Python's `datetime` module.

UTC timestamps provide consistent time references for storage, sorting, preprocessing, and historical analysis.

## 6. Data Collection and Processing

The collector records cumulative disk and network byte counters.

These counters are not transfer rates. The preprocessing layer calculates read, write, upload, and download rates by comparing consecutive telemetry records and their timestamps.

This separation keeps system data collection independent from feature engineering.

## 7. Error Handling

The collector handles unavailable disk or network I/O counters by using zero values when the corresponding `psutil` counter is unavailable.

Process enumeration also handles `NoSuchProcess` and `AccessDenied` exceptions when identifying top processes.

## 8. Testing

Unit tests verify:

- TelemetryRecord creation.
- SystemCollector output type.
- Validity of collected metric ranges.

The collector is tested independently to ensure that it produces valid telemetry records.

## 9. Continuous Collection Experiment

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

The effective sampling interval was approximately 5.21 seconds per sample. The difference from the configured interval was caused by the time required to collect and store each telemetry record before the sleep interval began.

### Initial Observation

The experiment demonstrated continuous collection and persistence of Linux telemetry into SQLite without runtime errors.

The measured database size indicated that SQLite was suitable for the initial single-machine implementation.

### Engineering Decision

The 5-second interval was treated as an initial experimental configuration rather than a final system requirement. Further experiments were planned to determine appropriate collection and aggregation intervals for anomaly detection and predictive analysis.

## 10. Current Implementation Status

The collector has been extended beyond the initial CPU and memory monitoring implementation.

The current implementation supports:

- CPU and memory monitoring.
- Swap and root filesystem monitoring.
- System load monitoring.
- Disk I/O counter collection.
- Network traffic counter collection.
- Process count monitoring.
- Identification of top CPU and memory-consuming processes.
- UTC timestamp generation.
- Structured telemetry records for downstream processing.

## 11. Conclusion

The telemetry collector provides the foundation of LinuxSentinel AI by gathering system performance information from the Linux operating system.

Its modular design separates data collection from preprocessing and machine-learning components, allowing the platform to be tested, maintained, and extended independently.
