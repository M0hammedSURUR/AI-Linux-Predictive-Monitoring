# Prediction Evaluation

## 1. Overview

Day 25 evaluates the LinuxSentinel AI prediction layer using a controlled telemetry dataset.

The evaluation measures prediction error using two standard regression metrics:

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)

The evaluation focuses on:

* CPU usage
* Memory usage
* Disk usage

The purpose is to measure how closely the predicted next value matches the actual next telemetry value.

## 2. Prediction Method

The current `TelemetryPredictor` uses a rolling linear trend based on up to five recent telemetry observations.

For each prediction:

1. Recent telemetry history is selected.
2. A linear trend is calculated from the observations.
3. The trend is extended by one step.
4. The predicted value is compared with the actual next telemetry value.

This provides a more stable prediction than relying only on the difference between two observations.

## 3. Evaluation Dataset

A deterministic controlled dataset containing ten telemetry observations was created for the experiment.

The dataset contains slightly irregular but generally increasing values to represent realistic measurement variation.

### CPU values

```
20.0, 23.0, 24.0, 28.0, 27.0,
32.0, 34.0, 35.0, 39.0, 40.0
```

### Memory values

```
40.0, 41.5, 42.0, 44.0, 43.5,
46.0, 47.5, 48.0, 50.0, 51.0
```

### Disk values

```
50.0, 50.8, 51.2, 52.5, 52.0,
53.5, 54.2, 55.0, 55.8, 57.0
```

The dataset is deterministic so that the experiment can be reproduced consistently.

## 4. Evaluation Metrics

### Mean Absolute Error

MAE measures the average absolute difference between predicted and actual values.

A lower MAE indicates that predictions are closer to the actual observations.

### Root Mean Squared Error

RMSE measures the square root of the average squared prediction error.

RMSE gives greater influence to larger prediction errors than MAE.

A lower RMSE therefore indicates better prediction performance and fewer large errors.

## 5. Evaluation Results

The prediction evaluation produced the following results:

| Metric       |    MAE |   RMSE |
| ------------ | -----: | -----: |
| CPU usage    | 1.9625 | 2.1889 |
| Memory usage | 0.9812 | 1.0722 |
| Disk usage   | 0.4837 | 0.6409 |

## 6. Result Analysis

The controlled experiment produced non-zero prediction errors, demonstrating that the evaluation is measuring prediction performance rather than reproducing a perfectly linear dataset.

CPU usage produced the highest prediction error in this experiment:

```
MAE: 1.9625
RMSE: 2.1889
```

Memory usage produced lower error:

```
MAE: 0.9812
RMSE: 1.0722
```

Disk usage produced the lowest error:

```
MAE: 0.4837
RMSE: 0.6409
```

The results indicate that the predictor followed the general telemetry trends while still showing differences between predicted and actual values.

These results are from a controlled evaluation dataset and should not be interpreted as production accuracy. Real-world performance should be evaluated using a larger dataset collected under different system workloads.

## 7. Automated Testing

A dedicated test was added in:

```
tests/test_prediction_evaluation.py
```

The test verifies that:

* Evaluation completes successfully.
* MAE values are non-negative.
* RMSE values are non-negative.
* The controlled dataset produces measurable non-zero prediction errors.

The evaluation test result was:

```
1 passed
```

The complete project test suite was also executed:

```
pytest -q
```

Final result:

```
62 passed in 3.13s
```

No existing project tests were broken by the prediction evaluation implementation.

## 8. Experiment Script

The reproducible evaluation experiment is located at:

```
experiments/prediction/evaluate_prediction.py
```

The script can be executed from the project root using:

```
PYTHONPATH=. python experiments/prediction/evaluate_prediction.py
```

The script prints MAE and RMSE values for CPU, memory, and disk prediction.

## 9. Limitations

The evaluation uses a small controlled dataset rather than a large production telemetry dataset.

The current prediction model is intentionally lightweight and is designed as an initial predictive layer.

The results should therefore be considered experimental rather than a definitive measurement of production prediction accuracy.

Future improvements can evaluate the predictor using larger historical telemetry datasets and compare it with more advanced forecasting models.

## 10. Conclusion

Day 25 established a measurable evaluation process for the LinuxSentinel AI prediction layer.

The system now provides:

* Rolling five-observation trend prediction
* Reproducible evaluation data
* MAE measurement
* RMSE measurement
* Automated evaluation testing
* Documented prediction results

This provides quantitative evidence for the prediction component and establishes a foundation for the final project evaluation and results section.
