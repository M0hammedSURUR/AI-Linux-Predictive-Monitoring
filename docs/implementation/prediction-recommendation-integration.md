# Prediction, Trend Forecasting, and Recommendation Integration

## 1. Overview

LinuxSentinel AI connects telemetry prediction with the recommendation engine and the human-approved self-healing workflow.

The prediction layer identifies metrics that may cross configured thresholds. High-risk predictions are passed to the recommendation engine, which generates a safe, human-readable recommendation.

No prediction directly executes a system action.

## 2. Prediction Layer

The `TelemetryPredictor` generates predictions from recent processed telemetry.

The current prediction layer uses a rolling linear-trend approach based on recent telemetry history.

The predictor uses up to the five most recent observations for:

- CPU usage
- Memory usage
- Disk usage

A linear trend is calculated from these recent observations, and the next value is estimated by extending the calculated trend by one step.

Using multiple recent observations reduces the influence of a single sudden measurement and provides a more stable prediction than using only the two most recent values.

Prediction risk levels are:

- `low`
- `medium`
- `high`

A high-risk prediction occurs when the predicted value reaches or exceeds its configured threshold.

## 3. Recommendation Layer

The `RecommendationEngine` converts high-risk predictions into recommendations.

For example:

- A predicted high CPU value produces a CPU monitoring recommendation.
- A predicted high memory value produces a memory investigation recommendation.
- A predicted high disk value produces a disk investigation recommendation.

Low-risk predictions do not generate recommendations.

## 4. Human-Approved Self-Healing

Recommendations are not automatically executed.

When a high-risk disk prediction is detected, the system can propose the predefined `clear_cache` action.

The action initially receives the status:

    PENDING

A human must explicitly approve the action before execution.

This preserves the project's human-in-the-loop safety requirement.

## 5. Simulation Mode

A dashboard simulation mode is available for safely testing the prediction-to-healing workflow.

The simulation creates a controlled high-risk disk prediction:

    Current value: 85%
    Predicted value: 95%
    Threshold: 90%

Simulation mode does not execute a real system action.

The simulated prediction is passed through the same recommendation and human-approval workflow used by the normal dashboard.

## 6. Integration Flow

    Telemetry
        |
        v
    Preprocessing
        |
        v
    Prediction
        |
        v
    Risk Assessment
        |
        v
    Recommendation
        |
        v
    Proposed Healing Action
        |
        v
    Human Approval
        |
        v
    Safe Self-Healing Execution

The ML anomaly detector remains an experimental signal and does not bypass this approval boundary.

## 7. Dashboard Verification

The dashboard was tested with Self-Healing Simulation enabled.

Observed behavior:

- Normal CPU prediction: low risk
- Normal memory prediction: low risk
- Normal disk prediction: low risk
- Simulated disk prediction: high risk
- One recommendation generated
- Proposed predefined action: `clear_cache`
- Healing status: `PENDING`
- No real system action executed automatically

The simulation prediction appeared only once after removing a duplicate dashboard append.

## 8. Testing

The existing prediction and recommendation tests were executed:

    pytest -q tests/test_prediction.py tests/test_recommendations.py

Result:

    10 passed

The complete project test suite was also executed:

    pytest -q

Result:

    60 passed

No existing tests were broken by the dashboard integration correction.

## 9. Safety Boundary

The prediction and recommendation layers cannot directly execute arbitrary system commands.

The self-healing workflow remains responsible for:

- Human approval
- Predefined action mapping
- Safety validation
- Audit logging
- Controlled execution

This separation ensures that prediction and recommendation remain advisory components.

## 10. Conclusion

The prediction-to-recommendation integration provides the next stage of the LinuxSentinel AI decision pipeline.

The system can now identify high-risk predicted conditions, generate recommendations, propose a predefined healing action, and wait for explicit human approval before any action is executed.
