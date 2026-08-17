# Telemetry Data Model

## 1. Purpose

The telemetry data model defines the structure used to store Linux system monitoring measurements collected by the telemetry collector.

The model provides a consistent representation of system observations and supports subsequent preprocessing, anomaly detection, predictive analysis, and historical monitoring.

## 2. Storage Technology

The initial implementation uses SQLite.

Database file:

`data/monitoring.db`

SQLite was selected because the project initially monitors a single Linux system and requires lightweight, local, transactional storage without the operational overhead of a separate database server.

## 3. Telemetry Entity

Each telemetry record represents one observation of the monitored Linux system at a specific UTC timestamp.

### Attributes

| Attribute | Type | Description |
|---|---|---|
| id | INTEGER | Unique telemetry record identifier |
| timestamp | TEXT | UTC timestamp of collection |
| cpu_percent | REAL | CPU utilization percentage |
| memory_percent | REAL | Memory utilization percentage |
| swap_percent | REAL | Swap utilization percentage |
| disk_percent | REAL | Disk space utilization percentage |
| load_1m | REAL | One-minute system load |
| disk_read_bytes | INTEGER | Cumulative disk bytes read |
| disk_write_bytes | INTEGER | Cumulative disk bytes written |
| network_bytes_sent | INTEGER | Cumulative network bytes sent |
| network_bytes_received | INTEGER | Cumulative network bytes received |
| process_count | INTEGER | Number of running processes |
| top_cpu_process | TEXT | Process identified by the collector for CPU usage |
| top_memory_process | TEXT | Process identified by the collector for memory usage |

## 4. Database Table

The primary table is:

`telemetry`

Each row represents one telemetry observation.

## 5. Primary Key

The `id` attribute is an auto-incrementing primary key.

This provides a unique identifier for each stored telemetry record.

## 6. Timestamp

Telemetry timestamps are stored in UTC.

A timestamp index is used because historical monitoring and machine-learning preprocessing will frequently require time-range queries.

## 7. Cumulative Metrics

Disk and network byte counters are stored as cumulative values obtained from the operating system.

The preprocessing layer can calculate interval-based rates from differences between consecutive observations.

Examples include:

- disk read rate
- disk write rate
- network upload rate
- network download rate

The raw cumulative counters are retained so that derived features can be recalculated when required.

## 8. Data Integrity

Required numerical telemetry attributes are stored as NOT NULL fields.

Process names are allowed to be NULL because process information may occasionally be unavailable or inaccessible.

## 9. Future Extensions

The current model intentionally focuses on the core telemetry required for the first implementation.

Future versions may introduce additional entities for:

- service status
- log events
- anomaly events
- predictions
- maintenance recommendations
- approved actions
- audit records

These entities will be added when their corresponding modules are implemented.
