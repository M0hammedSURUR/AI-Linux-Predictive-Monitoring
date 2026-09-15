from dataclasses import dataclass
import subprocess


@dataclass
class JournalEntry:
    """Represent one Linux journal entry."""

    timestamp: str
    source: str
    message: str


class JournalMonitor:
    """Read selected warning and error entries from systemd journal."""

    def __init__(self, limit: int = 10):
        if limit < 1:
            raise ValueError("Journal entry limit must be at least 1.")

        self.limit = limit

    def get_recent_warnings_and_errors(self) -> list[JournalEntry]:
        """Return recent warning and error journal entries."""

        result = subprocess.run(
            [
                "journalctl",
                "-p",
                "warning..err",
                "-n",
                str(self.limit),
                "--no-pager",
                "-o",
                "short-iso",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return []

        entries = []

        for line in result.stdout.splitlines():
            entry = self._parse_line(line)

            if entry is not None:
                entries.append(entry)

        return entries

    @staticmethod
    def _parse_line(line: str) -> JournalEntry | None:
        """Parse one journalctl short-iso line."""

        parts = line.split(maxsplit=3)

        if len(parts) < 4:
            return None

        timestamp = parts[0]
        source = parts[2].rstrip(":")
        message = parts[3]

        return JournalEntry(
            timestamp=timestamp,
            source=source,
            message=message,
        )
