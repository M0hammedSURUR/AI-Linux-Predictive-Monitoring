# Telemetry Preprocessing Design

## 1. Purpose

The preprocessing layer converts raw telemetry records stored in SQLite into validated and analysis-ready data for anomaly detection and predictive analysis.

## 2. Input

The preprocessing layer reads telemetry records from the `telemetry` table in the SQLite database.

The input contains:

- CPU utilization
- memory utilization
- swap utilization
- disk utilization
- one-minute load
- cumulative disk read bytes
- cumulative disk write bytes
- cumulative network bytes sent
- cumulative network bytes received
- process count
- top CPU process
- top memory process
- UTC timestamp

## 3. Processing Operations

The preprocessing layer performs the following operations:

1. Load telemetry records.
2. Sort records by timestamp.
3. Validate required numerical values.
4. Detect missing or invalid observations.
5. Calculate the time interval between consecutive observations.
6. Calculate disk read and write rates from cumulative counters.
7. Calculate network send and receive rates from cumulative counters.
8. Preserve the original telemetry values.
9. Produce analysis-ready features for downstream intelligence modules.

## 4. Derived Features

The following derived features are planned:

- time_delta_seconds
- disk_read_rate
- disk_write_rate
- network_send_rate
- network_receive_rate

Rates are calculated from differences between consecutive cumulative counter values divided by the elapsed time.

## 5. Data Integrity

Invalid negative counter differences will not be silently treated as valid rates.

Counter resets or other discontinuities will be detected and handled by the preprocessing layer.

## 6. Output

The preprocessing layer will provide a structured feature dataset that can be consumed by:

- anomaly detection
- prediction
- intelligence
- dashboard
- reporting

## 7. Design Principle

Raw telemetry is retained unchanged in the database.

Derived features are generated during preprocessing so that feature calculations can be revised without losing the original observations.
