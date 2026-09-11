import numpy as np
from sklearn.ensemble import IsolationForest


def test_isolation_forest_can_detect_an_outlier():
    """Verify that Isolation Forest can identify an injected outlier."""

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

    outlier = np.array([[99.0, 95.0, 99.0, 15.0]])

    data = np.vstack([normal_data, outlier])

    model = IsolationForest(
        contamination="auto",
        random_state=42,
    )

    model.fit(data)

    prediction = model.predict(outlier)

    assert prediction[0] == -1
