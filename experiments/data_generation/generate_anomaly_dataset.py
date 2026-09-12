import csv
import random
from pathlib import Path


OUTPUT_FILE = Path("data/samples/anomaly_dataset.csv")

NORMAL_RECORDS = 100
ANOMALY_RECORDS = 30

random.seed(42)


def generate_normal_record():
    """Generate realistic normal Linux telemetry."""

    return {
        "cpu_percent": round(random.uniform(5, 35), 2),
        "memory_percent": round(random.uniform(25, 55), 2),
        "disk_percent": round(random.uniform(8, 20), 2),
        "load_1m": round(random.uniform(0.1, 1.5), 2),
        "label": 0,
    }


def generate_anomaly_record():
    """Generate controlled abnormal Linux telemetry."""

    return {
        "cpu_percent": round(random.uniform(85, 100), 2),
        "memory_percent": round(random.uniform(80, 98), 2),
        "disk_percent": round(random.uniform(85, 99), 2),
        "load_1m": round(random.uniform(4.0, 10.0), 2),
        "label": 1,
    }


def main():
    """Generate and save a labelled anomaly dataset."""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    records = []

    for _ in range(NORMAL_RECORDS):
        records.append(generate_normal_record())

    for _ in range(ANOMALY_RECORDS):
        records.append(generate_anomaly_record())

    random.shuffle(records)

    fieldnames = [
        "cpu_percent",
        "memory_percent",
        "disk_percent",
        "load_1m",
        "label",
    ]

    with OUTPUT_FILE.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(records)

    print("Synthetic anomaly dataset generated")
    print("=" * 40)
    print(f"Normal records: {NORMAL_RECORDS}")
    print(f"Anomaly records: {ANOMALY_RECORDS}")
    print(f"Total records: {len(records)}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
