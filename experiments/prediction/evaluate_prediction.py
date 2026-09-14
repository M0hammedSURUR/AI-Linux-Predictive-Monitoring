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


def evaluate_scenario(
    scenario_name: str,
    cpu_values: list[float],
    memory_values: list[float],
    disk_values: list[float],
) -> None:
    """Evaluate prediction performance for one telemetry scenario."""

    base_timestamp = datetime.now(timezone.utc)

    records = []

    for index in range(len(cpu_values)):
        records.append(
            create_record(
                timestamp=base_timestamp + timedelta(seconds=index),
                cpu_percent=cpu_values[index],
                memory_percent=memory_values[index],
                disk_percent=disk_values[index],
            )
        )

    predictor = TelemetryPredictor()

    print(f"\nScenario: {scenario_name}")
    print("-" * 48)

    for metric in [
        "cpu_percent",
        "memory_percent",
        "disk_percent",
    ]:
        mae, rmse = evaluate_metric(
            predictor=predictor,
            records=records,
            metric=metric,
        )

        print(f"{metric}: MAE={mae:.4f}, RMSE={rmse:.4f}")


def main() -> None:
    """Run prediction evaluation across multiple trend scenarios."""

    evaluate_scenario(
        scenario_name="Increasing resource usage",
        cpu_values=[20, 23, 25, 29, 31, 34, 37, 40, 42, 45],
        memory_values=[40, 41, 43, 44, 46, 47, 49, 50, 52, 53],
        disk_values=[50, 51, 51.5, 52.5, 53, 54, 55, 55.5, 57, 58],
    )

    evaluate_scenario(
        scenario_name="Decreasing resource usage",
        cpu_values=[45, 42, 40, 38, 35, 33, 30, 28, 25, 23],
        memory_values=[60, 58, 57, 55, 53, 52, 50, 48, 47, 45],
        disk_values=[70, 68, 67, 65, 63, 61, 60, 58, 57, 55],
    )

    evaluate_scenario(
        scenario_name="Stable resource usage",
        cpu_values=[30, 30.5, 29.8, 30.2, 29.9, 30.1, 30.0, 30.3, 29.7, 30.1],
        memory_values=[45, 45.2, 44.8, 45.1, 45.0, 44.9, 45.1, 45.0, 44.8, 45.2],
        disk_values=[55, 55.1, 54.9, 55.0, 55.2, 54.8, 55.1, 55.0, 54.9, 55.1],
    )

    evaluate_scenario(
        scenario_name="Irregular resource usage",
        cpu_values=[20, 35, 25, 40, 30, 45, 28, 42, 32, 50],
        memory_values=[40, 48, 43, 52, 45, 55, 47, 53, 50, 58],
        disk_values=[50, 52, 51, 54, 53, 56, 55, 57, 56, 59],
    )


if __name__ == "__main__":
    main()
