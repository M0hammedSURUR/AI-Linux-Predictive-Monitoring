# ML-Based Anomaly Detection

## 1. Overview

The LinuxSentinel AI platform uses anomaly detection to identify unusual system behavior.

The project currently uses a rule-based anomaly detector as the primary safety mechanism. A machine-learning-based detector has been added as an experimental baseline to investigate learned detection of unusual telemetry patterns.

The ML detector is kept separate from the production healing workflow at this stage because the available telemetry dataset is still small.

## 2. ML Approach

The initial ML experiment uses the Isolation Forest algorithm from scikit-learn.

Isolation Forest is an unsupervised anomaly detection algorithm. It identifies observations that are easier to isolate from the rest of the dataset and assigns them lower anomaly scores.

The experiment does not require manually labelled anomaly data.

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

The model uses a fixed random state of `42` to make the experiment reproducible.

## 5. Experimental Result

At the time of testing, the monitoring database contained 35 telemetry records.

The baseline experiment produced:

* Telemetry records: 35
* Features: 4
* ML-detected outliers: 11

The experiment completed successfully without runtime errors.

These 11 records should be interpreted as **ML-detected outliers**, not as confirmed system failures. The current dataset is small and represents mostly stable system activity.

Therefore, this experiment demonstrates that the ML pipeline is operational, but it does not provide sufficient evidence to measure production anomaly-detection accuracy.

## 6. Automated Testing

An automated test was added in:

```text
tests/test_ml_baseline.py
```

The test uses controlled synthetic telemetry containing normal observations and an intentionally injected outlier.

The Isolation Forest model successfully classified the injected abnormal observation as an anomaly.

Test result:

```text
1 passed
```

The complete project test suite was also executed successfully:

```text
54 passed in 2.54s
```

## 7. Safety and Production Integration

The ML detector is currently an experimental component.

It does not directly trigger self-healing actions.

The existing rule-based detector remains responsible for known threshold-based abnormal conditions and provides the safer foundation for the current human-approved healing workflow.

The intended architecture is:

```text
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
```

The ML detector can therefore provide additional evidence about unusual system behavior without bypassing the human approval mechanism.

## 8. Current Limitations

The current ML baseline has several limitations:

* The available telemetry dataset is small.
* The data contains mostly normal system activity.
* There are no manually labelled anomaly records.
* Model performance cannot yet be evaluated reliably using accuracy, precision, recall, or F1-score.
* The detected outliers have not been independently validated as real system failures.
* The current experiment uses a basic feature set.

Because of these limitations, the ML baseline should be considered an experimental proof of concept rather than a production-ready anomaly detector.

## 9. Future Improvements

Future development will focus on:

* Collecting a larger and more diverse telemetry dataset.
* Generating controlled system-stress experiments.
* Creating labelled normal and abnormal observations.
* Comparing ML predictions with known failure conditions.
* Evaluating precision, recall, F1-score, and false-positive rate.
* Experimenting with additional telemetry features.
* Comparing Isolation Forest with other suitable anomaly-detection techniques.
* Combining ML results with the existing rule-based detector.
* Integrating validated ML results into the recommendation pipeline.

## 10. Dependencies

The ML baseline uses:

```text
scikit-learn==1.9.1
numpy==2.5.3
```

These dependencies are recorded explicitly in `requirements.txt` for reproducibility.
