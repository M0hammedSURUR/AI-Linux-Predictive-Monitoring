from .system_collector import SystemCollector


def main() -> None:
    collector = SystemCollector()
    record = collector.collect()

    print(record)


if __name__ == "__main__":
    main()
