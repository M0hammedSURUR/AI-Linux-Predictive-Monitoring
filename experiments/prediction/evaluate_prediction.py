from datetime import datetime, timedelta, timezone
from math import sqrt

from src.preprocessing.telemetry_preprocessor import ProcessedTelemetry
from src.prediction.predictor import TelemetryPredictor


def create_record(
    timestamp: datetime,
    cpu_percent: float,
    memory_percent: float,
    disk_percent: float,
) -> ProcessedTelemetry:
    """Create a sample processed telemetry record."""

    return ProcessedTelemetry(
        timestamp=timestamp,
        cpu_percent=cpu_percent,
        memory_percent=memory_percent,
        swap_percent=0.0,
        disk_percent=disk_percent,
        load_1m=0.5,
        process_count=100,
        disk_read_rate=100.0,
        disk_write_rate=100.0,
        network_send_rate=100.0,
        network_receive_rate=100.0,
        top_cpu_process="test_cpu",
        top_memory_process="test_memory",
    )


def mean_absolute_error(actual: list[float], predicted: list[float]) -> float:
    """Calculate Mean Absolute Error."""

    errors = [
        abs(actual_value - predicted_value)
        for actual_value, predicted_value in zip(actual, predicted)
    ]

    return sum(errors) / len(errors)


def root_mean_squared_error(
    actual: list[float],
    predicted: list[float],
) -> float:
    """Calculate Root Mean Squared Error."""

    squared_errors = [
        (actual_value - predicted_value) ** 2
        for actual_value, predicted_value in zip(actual, predicted)
    ]

    return sqrt(sum(squared_errors) / len(squared_errors))


def evaluate_metric(
    predictor: TelemetryPredictor,
    records: list[ProcessedTelemetry],
    metric: str,
) -> tuple[float, float]:
    """Evaluate one metric using one-step-ahead predictions."""

    actual_values = []
    predicted_values = []

    for index in range(2, len(records)):
        history = records[:index]

        predictions = predictor.predict(history)

        prediction = next(
            result
            for result in predictions
            if result.metric == metric
        )

        actual_value = getattr(records[index], metric)

        actual_values.append(actual_value)
        predicted_values.append(prediction.predicted_value)

    mae = mean_absolute_error(
        actual_values,
        predicted_values,
    )

    rmse = root_mean_squared_error(
        actual_values,
        predicted_values,
    )

    return mae, rmse


def main() -> None:
    """Run the prediction evaluation experiment."""

    base_timestamp = datetime.now(timezone.utc)

    records = []

    cpu_values = [20.0, 23.0, 24.0, 28.0, 27.0, 32.0, 34.0, 35.0, 39.0, 40.0]
    memory_values = [40.0, 41.5, 42.0, 44.0, 43.5, 46.0, 47.5, 48.0, 50.0, 51.0]
    disk_values = [50.0, 50.8, 51.2, 52.5, 52.0, 53.5, 54.2, 55.0, 55.8, 57.0]

    for index in range(10):
        records.append(
            create_record(
                timestamp=base_timestamp + timedelta(seconds=index),
                cpu_percent=cpu_values[index],
                memory_percent=memory_values[index],
                disk_percent=disk_values[index],
            )
        )

    predictor = TelemetryPredictor()

    metrics = [
        "cpu_percent",
        "memory_percent",
        "disk_percent",
    ]

    print("LinuxSentinel AI - Prediction Evaluation")
    print("=" * 48)

    for metric in metrics:
        mae, rmse = evaluate_metric(
            predictor=predictor,
            records=records,
            metric=metric,
        )

        print(f"\nMetric: {metric}")
        print(f"MAE:  {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")


if __name__ == "__main__":
    main()
