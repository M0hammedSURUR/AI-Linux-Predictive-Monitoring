from src.database.repository import TelemetryRepository
from src.preprocessing.telemetry_preprocessor import TelemetryPreprocessor


def test_preprocessor_returns_processed_records():
    repository = TelemetryRepository()
    preprocessor = TelemetryPreprocessor(repository)

    records = preprocessor.process()

    assert len(records) >= 1


def test_processed_records_contain_derived_rates():
    repository = TelemetryRepository()
    preprocessor = TelemetryPreprocessor(repository)

    records = preprocessor.process()

    assert records

    record = records[0]

    assert record.disk_read_rate >= 0
    assert record.disk_write_rate >= 0
    assert record.network_send_rate >= 0
    assert record.network_receive_rate >= 0


def test_processed_records_preserve_core_metrics():
    repository = TelemetryRepository()
    preprocessor = TelemetryPreprocessor(repository)

    records = preprocessor.process()

    assert records

    record = records[0]

    assert 0 <= record.cpu_percent <= 100
    assert 0 <= record.memory_percent <= 100
    assert record.process_count >= 0
