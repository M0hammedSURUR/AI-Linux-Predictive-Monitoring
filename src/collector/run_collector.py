import time

from src.collector.system_collector import SystemCollector
from src.database.repository import TelemetryRepository


COLLECTION_INTERVAL_SECONDS = 5


def main():
    collector = SystemCollector()
    repository = TelemetryRepository()

    print("Starting continuous telemetry collection...")
    print(f"Collection interval: {COLLECTION_INTERVAL_SECONDS} seconds")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            record = collector.collect()
            repository.save(record)

            print(
                f"{record.timestamp.isoformat()} | "
                f"CPU: {record.cpu_percent:.1f}% | "
                f"RAM: {record.memory_percent:.1f}% | "
                f"Disk: {record.disk_percent:.1f}% | "
                f"Load: {record.load_1m:.2f} | "
                f"Processes: {record.process_count}"
            )

            time.sleep(COLLECTION_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nTelemetry collection stopped.")


if __name__ == "__main__":
    main()
