# Collector Overhead Experiment

## Objective

To measure the execution time of one telemetry collection cycle and evaluate whether continuous system monitoring can be performed without significant computational overhead.

## Environment

- Operating System: Linux Mint 22.3 Cinnamon
- Python: 3.12.3
- CPU: AMD Ryzen 3 7320U
- CPU Cores/Threads: 8
- RAM: 7.1 GiB
- Python Environment: Virtual Environment (.venv)

## Experimental Method

The telemetry collector was executed 30 times.

The execution time of each collection cycle was measured using Python's `time.perf_counter()`.

## Results

| Metric | Result |
|---|---:|
| Number of samples | 30 |
| Mean execution time | 145.242 ms |
| Median execution time | 144.836 ms |
| Minimum execution time | 144.428 ms |
| Maximum execution time | 156.275 ms |

## Observation

The collector required approximately 145 ms per telemetry collection cycle.

The difference between the minimum and maximum execution times was approximately 11.85 ms, indicating relatively stable execution time during the experiment.

## Engineering Interpretation

The measured execution time indicates that a 1-second collection interval is technically feasible on the development machine.

However, the final telemetry collection interval will be determined after considering data volume, storage requirements, anomaly detection requirements, and prediction requirements.

## Conclusion

The telemetry collector demonstrates sufficiently low and stable execution time for continuous monitoring experiments on the development system.

The measurement will be used as evidence when selecting the final telemetry collection interval.
