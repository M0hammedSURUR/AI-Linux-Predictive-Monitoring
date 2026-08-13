from src.collector.system_collector import SystemCollector
from src.collector.models import TelemetryRecord


def test_system_collector_returns_telemetry_record():
    collector = SystemCollector()

    record = collector.collect()

    assert isinstance(record, TelemetryRecord)


def test_system_collector_values_are_valid():
    collector = SystemCollector()

    record = collector.collect()

    assert 0.0 <= record.cpu_percent <= 100.0
    assert 0.0 <= record.memory_percent <= 100.0
    assert 0.0 <= record.swap_percent <= 100.0
    assert 0.0 <= record.disk_percent <= 100.0
    assert record.load_1m >= 0.0
