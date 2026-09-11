import sqlite3

import numpy as np
from sklearn.ensemble import IsolationForest


DATABASE_PATH = "data/monitoring.db"

FEATURE_COLUMNS = [
    "cpu_percent",
    "memory_percent",
    "disk_percent",
    "load_1m",
]


def load_telemetry():
    """Load telemetry records from the project database."""

    connection = sqlite3.connect(DATABASE_PATH)

    query = """
        SELECT cpu_percent, memory_percent, disk_percent, load_1m
        FROM telemetry
        ORDER BY timestamp
    """

    rows = connection.execute(query).fetchall()
    connection.close()

    return np.array(rows, dtype=float)


def main():
    """Train and run the baseline ML anomaly detector."""

    data = load_telemetry()

    if len(data) < 10:
        raise ValueError(
            "At least 10 telemetry records are required "
            "for the ML baseline experiment."
        )

    model = IsolationForest(
        contamination="auto",
        random_state=42,
    )

    model.fit(data)

    predictions = model.predict(data)
    scores = model.decision_function(data)

    anomaly_count = int(np.sum(predictions == -1))

    print("ML Anomaly Detection Baseline")
    print("=" * 32)
    print(f"Telemetry records: {len(data)}")
    print(f"Features: {', '.join(FEATURE_COLUMNS)}")
    print(f"Detected anomalies: {anomaly_count}")
    print()

    for index, prediction in enumerate(predictions):
        status = "ANOMALY" if prediction == -1 else "NORMAL"

        print(
            f"Record {index + 1:02d}: "
            f"{status:<7} "
            f"score={scores[index]:.4f}"
        )


if __name__ == "__main__":
    main()
