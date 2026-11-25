# Telemetry Preprocessing Design

## 1. Purpose

The preprocessing layer converts raw telemetry records stored in SQLite into validated and analysis-ready data for anomaly detection, predictive analysis, and dashboard visualization.

It also derives network and disk I/O rates from cumulative system counters.

## 2. Input

The preprocessing layer reads telemetry records from the SQLite database.

The input contains:

- CPU utilization
- Memory utilization
- Swap utilization
- Disk utilization
- One-minute system load
- Cumulative disk read bytes
- Cumulative disk write bytes
- Cumulative network bytes sent
- Cumulative network bytes received
- Process count
- Top CPU-consuming process
- Top memory-consuming process
- UTC timestamp

## 3. Processing Operations

The preprocessing layer performs the following operations:

1. Load telemetry records.
2. Sort records by timestamp.
3. Validate required numerical values.
4. Handle missing or invalid observations.
5. Calculate the time interval between consecutive observations.
6. Calculate disk read and write rates from cumulative counters.
7. Calculate network upload and download rates from cumulative counters.
8. Preserve original telemetry values.
9. Produce structured features for downstream components.

## 4. Derived Features

The preprocessing layer generates the following derived features:

| Feature | Description | Unit |
|---|---|---|
| time_delta_seconds | Time between consecutive samples | Seconds |
| disk_read_rate | Disk read speed | Bytes/second |
| disk_write_rate | Disk write speed | Bytes/second |
| network_send_rate | Network upload speed | Bytes/second |
| network_receive_rate | Network download speed | Bytes/second |

Rates are calculated using:

```text
Rate = (Current Counter - Previous Counter) / Time Difference
```

The first record does not have a previous sample for comparison. Therefore, rate calculation requires a subsequent telemetry observation.

## 5. Data Integrity and Validation

The preprocessing layer applies the following safeguards:

- Handles missing or invalid observations.
- Detects counter resets and discontinuities.
- Prevents invalid negative counter differences from being treated as valid rates.
- Handles zero or invalid time intervals safely.
- Retains original telemetry records in the database.

When a counter reset is detected, the corresponding rate is handled safely rather than producing an invalid negative value.

## 6. Process Monitoring Features

Process-related information is preserved in the processed telemetry output.

The following fields support dashboard monitoring:

- `process_count`
- `top_cpu_process`
- `top_memory_process`

These features help identify the processes currently consuming the most CPU and memory resources.

## 7. Output

The preprocessing layer produces structured telemetry features containing:

- CPU, memory, swap, and disk utilization
- System load
- Process count
- Network upload and download rates
- Disk read and write rates
- Top CPU-consuming process
- Top memory-consuming process
- Timestamp

The processed telemetry is consumed by:

- Anomaly detection
- Predictive monitoring
- Intelligence and recommendation modules
- Streamlit dashboard
- Reporting and analysis

## 8. Dashboard Integration

The dashboard uses processed telemetry to display:

- Network upload and download metrics
- Disk read and write metrics
- Network I/O trend charts
- Disk I/O trend charts
- Process count
- Top CPU-consuming process
- Top memory-consuming process

Network and disk I/O rates are displayed in KB/s after conversion from bytes per second.

## 9. Design Principles

1. Raw telemetry is retained unchanged in the database.
2. Derived features are generated during preprocessing.
3. Processing must handle counter resets and invalid observations safely.
4. Original timestamps are preserved.
5. Preprocessing remains separate from anomaly detection and prediction logic.
6. The same processed data can support monitoring, analysis, and visualization.

## 10. Conclusion

The preprocessing layer provides a structured and reusable transformation between raw Linux telemetry and downstream intelligence components.

It enables LinuxSentinel AI to monitor not only CPU, memory, disk utilization, and system load, but also network activity, disk I/O performance, and process resource consumption.
