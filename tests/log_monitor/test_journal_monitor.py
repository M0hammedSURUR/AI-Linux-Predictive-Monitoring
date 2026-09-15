from src.log_monitor.journal_monitor import JournalMonitor


def test_journal_monitor_returns_entries():
    monitor = JournalMonitor(limit=5)

    entries = monitor.get_recent_warnings_and_errors()

    assert isinstance(entries, list)

    for entry in entries:
        assert entry.timestamp
        assert entry.source
        assert entry.message


def test_journal_monitor_rejects_invalid_limit():
    try:
        JournalMonitor(limit=0)
        assert False
    except ValueError:
        assert True


def test_journal_entry_limit_is_stored():
    monitor = JournalMonitor(limit=7)

    assert monitor.limit == 7
