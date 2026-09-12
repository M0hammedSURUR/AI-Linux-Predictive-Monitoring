import numpy as np

from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)


def test_isolation_forest_evaluation_metrics():
    """Verify that the ML evaluation produces valid metrics."""

    normal_data = np.array(
        [
            [10.0, 30.0, 40.0, 0.5],
            [12.0, 31.0, 41.0, 0.6],
            [11.0, 29.0, 39.0, 0.4],
            [13.0, 30.0, 42.0, 0.7],
            [10.0, 32.0, 40.0, 0.5],
            [12.0, 31.0, 41.0, 0.6],
            [11.0, 30.0, 40.0, 0.5],
            [13.0, 29.0, 42.0, 0.7],
            [10.0, 31.0, 39.0, 0.4],
            [12.0, 30.0, 41.0, 0.6],
        ]
    )

    anomaly_data = np.array(
        [
            [99.0, 95.0, 99.0, 15.0],
            [97.0, 92.0, 98.0, 12.0],
        ]
    )

    features = np.vstack(
        [normal_data, anomaly_data]
    )

    labels = np.array(
        [0] * len(normal_data)
        + [1] * len(anomaly_data)
    )

    model = IsolationForest(
        contamination=0.17,
        random_state=42,
    )

    model.fit(features)

    predictions = model.predict(features)

    predicted_labels = np.where(
        predictions == -1,
        1,
        0,
    )

    accuracy = accuracy_score(
        labels,
        predicted_labels,
    )

    precision = precision_score(
        labels,
        predicted_labels,
    )

    recall = recall_score(
        labels,
        predicted_labels,
    )

    f1 = f1_score(
        labels,
        predicted_labels,
    )

    assert 0.0 <= accuracy <= 1.0
    assert 0.0 <= precision <= 1.0
    assert 0.0 <= recall <= 1.0
    assert 0.0 <= f1 <= 1.0

    assert predicted_labels[-1] == 1
    assert predicted_labels[-2] == 1
