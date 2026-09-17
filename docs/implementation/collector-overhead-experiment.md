# Collector and Platform Overhead Experiment

## Objective

To measure the execution time and runtime resource usage of the LinuxSentinel AI monitoring platform and evaluate whether continuous system monitoring can be performed without significant computational overhead.

The experiment considers both the telemetry collector and the Streamlit monitoring dashboard.

## Environment

- Operating System: Linux Mint 22.3 Cinnamon
- Python: 3.12.3
- CPU: AMD Ryzen 3 7320U
- CPU Cores/Threads: 8
- RAM: 7.1 GiB
- Python Environment: Virtual Environment (.venv)
- Streamlit: 1.63.0

## Experimental Method

Two types of measurements were performed.

### Collection Cycle Timing

The telemetry collector was executed 30 times.

The execution time of each collection cycle was measured using Python's `time.perf_counter()`.

### Runtime Resource Usage

The continuous telemetry collector and dashboard were allowed to run for several minutes before measuring their resource usage.

Linux `ps` was used to record:

- CPU utilization
- Memory utilization
- Resident Set Size (RSS)
- Process runtime

The collector and dashboard were measured separately and then measured together.

## Collection Cycle Results

| Metric | Result |
|---|---:|
| Number of samples | 30 |
| Mean execution time | 145.242 ms |
| Median execution time | 144.836 ms |
| Minimum execution time | 144.428 ms |
| Maximum execution time | 156.275 ms |

The collector required approximately 145 ms per telemetry collection cycle.

The difference between the minimum and maximum execution times was approximately 11.85 ms, indicating relatively stable execution time during the experiment.

## Runtime Resource Usage Results

### Telemetry Collector

The collector was continuously executed for more than five minutes before measurement.

| Metric | Result |
|---|---:|
| CPU utilization | 0.9% |
| Memory utilization | 0.3% |
| RSS memory | 27,388 KB (~26.7 MB) |
| Runtime at measurement | 6 min 23 sec |

### Streamlit Dashboard

The dashboard was continuously executed for approximately six minutes before measurement.

| Metric | Result |
|---|---:|
| CPU utilization | 9.9% |
| Memory utilization | 3.4% |
| RSS memory | 252,268 KB (~246.4 MB) |
| Runtime at measurement | 6 min |

### Combined Monitoring Platform

The collector and dashboard were measured while both were running.

| Metric | Result |
|---|---:|
| Combined CPU utilization | 10.8% |
| Combined memory utilization | 3.7% |
| Combined RSS memory | ~273.1 MB |

The combined CPU value is the sum of the measured collector and dashboard CPU values. The combined RSS value is the sum of their measured resident memory values.

## Observation

The telemetry collector demonstrated low runtime resource usage, consuming approximately 0.9% CPU and 26.7 MB of resident memory during the measurement.

The Streamlit dashboard consumed more resources than the collector, with approximately 9.9% CPU and 246.4 MB of resident memory.

The dashboard's higher resource usage is expected because it continuously performs visualization, data processing, anomaly detection, prediction, and user-interface updates.

## Engineering Interpretation

The collection-cycle timing indicates that the collector can complete a telemetry collection cycle in approximately 145 ms.

The runtime measurements show that the collector itself has a relatively small resource footprint compared with the available system resources.

The dashboard has a larger runtime footprint because it provides the interactive monitoring interface and performs additional processing.

These measurements demonstrate the observed resource characteristics of the prototype on the development machine. They should not be interpreted as universal performance limits because resource usage can vary with hardware, workload, monitoring interval, data volume, and dashboard activity.

## Limitations

The measurements represent a prototype evaluation on one development system.

CPU and memory usage can vary depending on:

- Background applications
- System workload
- Number of stored telemetry records
- Monitoring interval
- Browser activity
- Dashboard refresh activity
- Machine hardware

Therefore, the results are reported as observed measurements rather than fixed performance guarantees.

## Conclusion

The LinuxSentinel AI prototype demonstrated measurable and manageable runtime overhead during the experiment.

The telemetry collector showed low CPU and memory usage, while the dashboard accounted for the majority of the measured application resource consumption.

Together with the collection-cycle timing experiment, these measurements provide evidence for the feasibility of continuous Linux system monitoring on the development machine.
