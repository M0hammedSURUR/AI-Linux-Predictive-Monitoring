# Log Monitoring Implementation

## 1. Overview

LinuxSentinel AI includes a read-only Linux log monitoring component for identifying recent warning and error messages from the system journal.

The implementation uses the `journalctl` utility through Python's `subprocess` module.

It retrieves selected journal entries without modifying or deleting system logs.

## 2. Implementation

The log monitoring component is implemented in:

```text
src/log_monitor/journal_monitor.py
```

The main components are:

- `JournalEntry` — a dataclass representing one journal entry.
- `JournalMonitor` — retrieves and parses recent warning and error entries.

The monitor executes a predefined command equivalent to:

```bash
journalctl -p warning..err -n 10 --no-pager -o short-iso
```

The command:

- Selects warning and error priority levels.
- Limits the number of retrieved entries.
- Disables interactive paging.
- Uses ISO-style timestamps.

## 3. Configuration

The default configuration retrieves the latest 10 warning/error entries:

```python
JournalMonitor(limit=10)
```

The entry limit can be changed through the `limit` parameter.

A value below 1 raises a `ValueError`, preventing invalid limits.

## 4. Extracted Information

Each journal entry is represented using three fields:

| Field | Description |
|---|---|
| `timestamp` | Date and time of the journal entry |
| `source` | Process or system component that generated the entry |
| `message` | Warning or error message |

The `_parse_line()` method separates the timestamp, source, and message from each `journalctl` output line.

Lines that do not contain enough information are ignored.

## 5. Error Handling

The monitor executes `journalctl` using Python's `subprocess.run()`.

The command output is captured as text.

If the command returns a non-zero exit code, the monitoring method returns an empty list.

This prevents command failures from being treated as valid journal entries.

The implementation also ignores output lines that cannot be parsed.

## 6. Dashboard Integration

The log monitor is integrated into the Streamlit dashboard under:

**Linux Log Monitoring**

The dashboard displays:

- Source
- Warning/error message
- Timestamp

Recent entries are presented as warning notifications so that potentially important system events are easily visible.

## 7. Safety Considerations

The implementation is intentionally read-only.

It:

- Does not modify system logs.
- Does not execute arbitrary commands supplied by users.
- Does not delete journal entries.
- Uses a predefined `journalctl` command.
- Limits the number of entries retrieved.
- Captures command output rather than displaying an interactive terminal.

## 8. Testing

Automated tests are located in:

```text
tests/log_monitor/test_journal_monitor.py
```

The tests verify:

1. Journal entries can be retrieved successfully.
2. Invalid entry limits are rejected.
3. The configured entry limit is stored correctly.

Historical test result:

```text
3 passed
```

The complete project test suite previously passed:

```text
69 passed
```

## 9. Real Linux Verification

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

The monitor successfully parsed timestamps, sources, and messages from real warning/error entries.

## 10. Requirement Mapping

This implementation satisfies:

**FR-08 — Monitor selected system/application logs.**

The requirement is implemented through read-only system journal monitoring and dashboard presentation of recent warning and error entries.

## 11. Conclusion

The log monitoring component provides LinuxSentinel AI with read-only access to selected system journal messages.

Its limited command execution, output parsing, and error handling support safe integration with the monitoring dashboard.
