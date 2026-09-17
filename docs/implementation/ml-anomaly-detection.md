# ML-Based Anomaly Detection

## 1. Overview

The LinuxSentinel AI platform uses anomaly detection to identify unusual system behavior.

The project currently uses a rule-based anomaly detector as the primary safety mechanism. A machine-learning-based detector has been added as an experimental baseline to investigate learned detection of unusual telemetry patterns.

The ML detector is kept separate from the production healing workflow because the available real-world telemetry dataset is still limited.

## 2. ML Approach

The initial ML experiment uses the Isolation Forest algorithm from scikit-learn.

Isolation Forest is an unsupervised anomaly detection algorithm. It identifies observations that are easier to isolate from the rest of the dataset and assigns lower anomaly scores.

The baseline model does not require manually labelled anomaly data during training.

## 3. Telemetry Features

The baseline model uses four system telemetry features:

* `cpu_percent` — CPU utilization percentage
* `memory_percent` — memory utilization percentage
* `disk_percent` — disk utilization percentage
* `load_1m` — one-minute system load average

The telemetry records are loaded from the project's SQLite monitoring database.

## 4. Experimental Implementation

The ML baseline is implemented in:

```text
experiments/anomaly_detection/ml_baseline.py
```
The experiment:

1. Loads telemetry records from the SQLite database.
2. Extracts the four selected features.
3. Trains an Isolation Forest model.
4. Generates anomaly predictions.
5. Calculates anomaly scores.
6. Reports the number of detected outliers.

The model uses a fixed random state of 42 to make the experiment reproducible.

## 5. Real Telemetry Experiment

At the time of the baseline experiment, the monitoring database contained 35 telemetry records.

The baseline experiment produced:

* Telemetry records: 35
* Features: 4
* ML-detected outliers: 11

The experiment completed successfully without runtime errors.

These 11 records should be interpreted as **ML-detected outliers**, not as confirmed system failures. The dataset mainly represents stable system activity and does not contain independently labelled failure events.

Therefore, this experiment demonstrates that the ML pipeline is operational, but it does not establish real-world anomaly-detection performance.

## 6. Controlled ML Evaluation

A separate controlled evaluation was implemented in:

tests/test_ml_evaluation.py

The evaluation uses a synthetic dataset containing:

* 10 normal observations
* 2 intentionally injected anomalous observations

The normal observations represent stable system telemetry, while the anomalous observations contain deliberately extreme CPU, memory, disk, and load values.

The Isolation Forest model was configured with:

contamination = 0.17
random_state = 42

The model was fitted to the controlled dataset and its predictions were compared with the known synthetic labels.

### Evaluation Metrics

| Metric | Result |
|---|---:|
| Accuracy | 1.0000 (100%) |
| Precision | 1.0000 (100%) |
| Recall | 1.0000 (100%) |
| F1-score | 1.0000 (100%) |
| Normal observations | 10 |
| Anomalous observations | 2 |
| Correctly detected anomalies | 2/2 |

The predicted labels exactly matched the controlled evaluation labels:

Actual labels:
[0 0 0 0 0 0 0 0 0 0 1 1]

Predicted labels:
[0 0 0 0 0 0 0 0 0 0 1 1]

The automated evaluation test completed successfully:

1 passed in 1.83s

### Interpretation

The controlled evaluation demonstrates that the configured Isolation Forest model successfully identified the deliberately extreme anomalous observations in the synthetic dataset.

The 100% metric values apply only to this controlled evaluation dataset. They should not be interpreted as production or real-world model accuracy.

Because the evaluation dataset is small, synthetic, deliberately separable, and evaluated using the same observations used for model fitting, the results are evidence of correct experimental behavior rather than a general performance guarantee.

## 7. Automated Testing

The ML evaluation test verifies that:

1. The Isolation Forest model can be trained successfully.
2. Predictions can be generated.
3. Accuracy, precision, recall, and F1-score are valid.
4. The intentionally injected anomalous observations are detected.

The targeted ML evaluation test produced:

tests/test_ml_evaluation.py::test_isolation_forest_evaluation_metrics PASSED

1 passed in 1.83s

The complete project test suite also passes successfully.

## 8. Safety and Production Integration

The ML detector is currently an experimental component.

It does not directly trigger self-healing actions.

The existing rule-based detector remains responsible for known threshold-based abnormal conditions and provides the safer foundation for the current human-approved healing workflow.

The intended architecture is:

Telemetry
    |
    +----------------------+
    |                      |
    v                      v
Rule-Based Detector    ML Detector
    |                      |
    |                      |
    +----------+-----------+
               |
               v
       Combined Analysis
               |
               v
        Recommendation
               |
               v
     Human Approval
               |
               v
        Self-Healing

The ML detector can therefore provide additional evidence about unusual system behavior without bypassing the human approval mechanism.

## 9. Current Limitations

The current ML baseline has several limitations:

* The available real-world telemetry dataset is small.
* The real telemetry data contains mostly normal system activity.
* There are no independently labelled real system failure records.
* The controlled evaluation uses synthetic observations.
* The controlled evaluation is small and deliberately separates normal and anomalous observations.
* The controlled evaluation uses the same observations for model fitting and evaluation.
* The current experiment therefore cannot establish production-level anomaly-detection performance.
* The current experiment uses a basic feature set.

The 100% metrics obtained during the controlled evaluation should therefore be treated as experimental evidence rather than a general accuracy claim.

## 10. Future Improvements

Future development will focus on:

* Collecting a larger and more diverse telemetry dataset.
* Generating controlled system-stress experiments.
* Creating labelled normal and abnormal observations.
* Separating training and evaluation datasets.
* Comparing ML predictions with known failure conditions.
* Evaluating precision, recall, F1-score, and false-positive rate on held-out data.
* Experimenting with additional telemetry features.
* Comparing Isolation Forest with other suitable anomaly-detection techniques.
* Combining ML results with the existing rule-based detector.
* Integrating validated ML results into the recommendation pipeline.

## 11. Dependencies

The ML baseline uses:

scikit-learn==1.9.1
numpy==2.5.3

These dependencies are recorded explicitly in requirements.txt for reproducibility.
