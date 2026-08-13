from datetime import datetime, timezone

from src.collector.models import TelemetryRecord


def test_telemetry_record_creation():
    timestamp = datetime.now(timezone.utc)

    record = TelemetryRecord(
        timestamp=timestamp,
        cpu_percent=25.0,
        memory_percent=40.0,
        swap_percent=0.0,
        disk_percent=50.0,
        load_1m=1.5,
    )

    assert record.timestamp == timestamp
    assert record.cpu_percent == 25.0
    assert record.memory_percent == 40.0
    assert record.swap_percent == 0.0
    assert record.disk_percent == 50.0
    assert record.load_1m == 1.5
