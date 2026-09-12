import csv
from pathlib import Path

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


DATASET_FILE = Path("data/samples/anomaly_dataset.csv")

FEATURE_COLUMNS = [
    "cpu_percent",
    "memory_percent",
    "disk_percent",
    "load_1m",
]


def load_dataset():
    """Load the labelled anomaly dataset."""

    features = []
    labels = []

    with DATASET_FILE.open("r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            features.append(
                [
                    float(row[column])
                    for column in FEATURE_COLUMNS
                ]
            )
            labels.append(int(row["label"]))

    return np.array(features), np.array(labels)


def main():
    """Train Isolation Forest and evaluate its predictions."""

    features, labels = load_dataset()

    model = IsolationForest(
        contamination=0.23,  # NEW: 30 anomalies / 130 records
        random_state=42,
    )

    model.fit(features)

    predictions = model.predict(features)

    # Isolation Forest uses -1 for anomaly and 1 for normal.
    predicted_labels = np.where(
        predictions == -1,
        1,
        0,
    )

    accuracy = accuracy_score(labels, predicted_labels)
    precision = precision_score(labels, predicted_labels)
    recall = recall_score(labels, predicted_labels)
    f1 = f1_score(labels, predicted_labels)

    matrix = confusion_matrix(labels, predicted_labels)

    print("ML Anomaly Detection Evaluation")
    print("=" * 35)
    print(f"Dataset records: {len(features)}")
    print(f"Actual normal records: {np.sum(labels == 0)}")
    print(f"Actual anomaly records: {np.sum(labels == 1)}")
    print()

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1-score : {f1:.4f}")
    print()

    print("Confusion Matrix")
    print("================")
    print(matrix)

    print()
    print("Matrix format:")
    print("[[True Negative, False Positive]")
    print(" [False Negative, True Positive]]")


if __name__ == "__main__":
    main()
