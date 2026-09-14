# Prediction Scenario Evaluation

## 1. Overview

Day 26 extends the prediction evaluation performed in Day 25.

The objective is to evaluate the telemetry predictor under different resource-usage patterns instead of testing only one dataset.

Four deterministic scenarios were evaluated:

1. Increasing resource usage
2. Decreasing resource usage
3. Stable resource usage
4. Irregular resource usage

The evaluation uses Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).

---

## 2. Evaluation Method

The existing `TelemetryPredictor` uses a rolling linear trend based on recent telemetry observations.

The predictor considers up to five recent observations when estimating the next value.

For each scenario, CPU, memory, and disk usage values were provided as deterministic synthetic telemetry data.

The prediction errors were calculated using:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

Lower values indicate better prediction accuracy.

---

## 3. Scenario Results

| Scenario | Metric | MAE | RMSE |
|---|---|---:|---:|
| Increasing | CPU | 0.6125 | 0.7770 |
| Increasing | Memory | 0.5750 | 0.5979 |
| Increasing | Disk | 0.3312 | 0.3779 |
| Decreasing | CPU | 0.6000 | 0.6265 |
| Decreasing | Memory | 0.5500 | 0.5916 |
| Decreasing | Disk | 0.5500 | 0.6042 |
| Stable | CPU | 0.4488 | 0.5572 |
| Stable | Memory | 0.2725 | 0.3230 |
| Stable | Disk | 0.2350 | 0.2586 |
| Irregular | CPU | 15.6875 | 16.3310 |
| Irregular | Memory | 8.0375 | 8.5205 |
| Irregular | Disk | 2.1125 | 2.1803 |

---

## 4. Results Analysis

### 4.1 Increasing Resource Usage

The predictor performed well on steadily increasing resource usage.

The errors remained relatively low across all three metrics, indicating that the rolling linear trend was able to follow the increasing pattern.

### 4.2 Decreasing Resource Usage

The predictor also performed well on decreasing resource usage.

The results demonstrate that the linear trend approach can model both upward and downward resource trends.

### 4.3 Stable Resource Usage

The stable scenario produced the lowest overall prediction errors.

This is expected because the resource values changed only slightly around a stable operating level.

The predictor therefore had a relatively consistent recent history from which to estimate the next value.

### 4.4 Irregular Resource Usage

The irregular scenario produced significantly higher errors, particularly for CPU usage.

This is an expected limitation of a linear trend predictor because sudden increases and decreases do not follow a consistent linear pattern.

---

## 5. Interpretation

The current rolling linear predictor is most suitable for telemetry with a relatively consistent trend.

Its performance is strong for:

- Stable resource usage
- Increasing resource usage
- Decreasing resource usage

Its performance decreases when telemetry becomes highly irregular.

This limitation is acceptable for the current project because the predictor is designed as a lightweight and interpretable forecasting component.

---

## 6. Testing

The dedicated prediction evaluation test passed successfully.

The complete project test suite also passed:

    62 passed in 3.57s

---

## 7. Implementation

The scenario evaluation is implemented in:

    experiments/prediction/evaluate_prediction.py

A reusable `evaluate_scenario()` function was introduced to evaluate multiple telemetry patterns using the same evaluation process.

This avoids duplicating evaluation logic for each scenario.

---

## 8. Limitations

The evaluation uses deterministic synthetic telemetry rather than a large real-world monitoring dataset.

The current predictor uses a simple rolling linear trend and therefore cannot reliably model highly irregular or nonlinear behavior.

Future work could investigate more advanced forecasting techniques if sufficient real telemetry data becomes available.

---

## 9. Conclusion

Day 26 improves the evaluation quality of the prediction component by testing it across multiple realistic resource-usage patterns.

The results show that the predictor performs well for stable and directional trends while showing higher error for irregular behavior.

The evaluation provides a clearer understanding of the strengths and limitations of the current prediction approach.
