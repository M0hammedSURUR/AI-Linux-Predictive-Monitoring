# Log Monitoring Implementation

## 1. Overview

The LinuxSentinel AI platform includes a read-only Linux log monitoring component for identifying recent warning and error messages from the system journal.

The implementation uses `journalctl` through Python's `subprocess` module and does not modify or delete system log entries.

## 2. Implementation

The log monitoring component is implemented in:

```text
src/log_monitor/journal_monitor.py
```

The main classes are:

* `JournalEntry` — represents one journal entry.
* `JournalMonitor` — retrieves recent warning and error entries.

The monitor uses:

```text
journalctl -p warning..err -n <limit> --no-pager -o short-iso
```

This restricts the retrieved entries to warning and error priority levels and limits the number of entries returned.

## 3. Configuration

The monitor currently retrieves the latest 10 warning/error entries:

```python
JournalMonitor(limit=10)
```

The limit is configurable through the `limit` parameter.

Invalid values below 1 are rejected.

## 4. Extracted Information

Each journal entry is represented using three fields:

| Field       | Description                                          |
| ----------- | ---------------------------------------------------- |
| `timestamp` | Date and time of the journal entry                   |
| `source`    | Process or system component that generated the entry |
| `message`   | Warning or error message                             |

## 5. Dashboard Integration

The log monitor is integrated into the Streamlit dashboard under:

**Linux Log Monitoring**

The dashboard displays:

* Source
* Warning/error message
* Timestamp

Recent entries are presented as warning notifications so that potentially important system events are easily visible.

## 6. Safety Considerations

The implementation is intentionally read-only.

It:

* Does not modify system logs.
* Does not execute arbitrary commands supplied by users.
* Does not delete journal entries.
* Uses a predefined `journalctl` command.
* Limits the number of entries retrieved.

## 7. Testing

Automated tests are located in:

```text
tests/log_monitor/test_journal_monitor.py
```

The current tests verify:

1. Journal entries can be retrieved successfully.
2. Invalid entry limits are rejected.
3. The configured entry limit is stored correctly.

Current result:

```text
3 passed
```

The complete project test suite currently passes:

```text
69 passed in 2.35s
```

## 8. Real Linux Verification

The component was verified against the actual Linux system journal.

Example sources observed during testing included:

```text
kernel
NetworkManager
generate
xdg-desktop-por
gvfsd-wsdd
gvfsd-network
```

The monitor successfully parsed the timestamp, source, and message from these real warning/error entries.

## 9. Requirement Mapping

This implementation satisfies:

**FR-08 — Monitor selected system/application logs.**

The requirement is implemented through read-only system journal monitoring and dashboard presentation of recent warning and error entries.
