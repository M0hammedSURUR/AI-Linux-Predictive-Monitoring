from pathlib import Path
from time import monotonic  # NEW

from src.self_healing.models import HealingAction


class SelfHealingExecutor:
    """Executes only predefined, approved healing actions."""

    ALLOWED_ACTIONS = {
        "clear_cache",
        "restart_service",
    }

    CACHE_DIRECTORY = Path.home() / ".cache"

    EXECUTION_TIMEOUT_SECONDS = 10

    def execute(self, action: HealingAction) -> str:
        """Execute an approved healing action."""

        if action.status != "approved":
            raise ValueError(
                "Only approved healing actions can be executed."
            )

        if action.action not in self.ALLOWED_ACTIONS:
            raise ValueError(
                f"Action '{action.action}' is not allowed."
            )

        # NEW: Record when execution starts.
        start_time = monotonic()

        if action.action == "clear_cache":
            result = self._clear_cache()

            # NEW: Measure the total execution duration.
            execution_duration = monotonic() - start_time

            # NEW: Report an execution-duration timeout condition.
            if execution_duration > self.EXECUTION_TIMEOUT_SECONDS:
                raise TimeoutError(
                    f"Healing action exceeded the configured "
                    f"execution time limit of "
                    f"{self.EXECUTION_TIMEOUT_SECONDS} seconds."
                )

            return result

        if action.action == "restart_service":
            raise ValueError(
                "Real service restart is not implemented yet."
            )

        raise ValueError(
            f"Unsupported healing action: {action.action}"
        )

    def _clear_cache(self) -> str:
        """Remove cache contents only from the approved cache directory."""

        cache_directory = self.CACHE_DIRECTORY.resolve()

        # NEW: Determine the only directory that is allowed for real execution.
        approved_cache_directory = (
            Path.home() / ".cache"
        ).resolve()

        # NEW: Prevent the executor from being redirected to another location.
        if cache_directory != approved_cache_directory:
            raise ValueError(
                "Cache cleanup target is outside the approved "
                "user cache directory."
            )

        if not cache_directory.exists():
            raise ValueError(
                "Cache directory does not exist."
            )

        if not cache_directory.is_dir():
            raise ValueError(
                "Cache path is not a directory."
            )

        deleted_items = 0
        failed_items = 0

        for item in cache_directory.iterdir():
            try:
                if item.is_dir() and not item.is_symlink():
                    self._remove_directory(item)
                else:
                    item.unlink()

                deleted_items += 1

            except OSError:
                failed_items += 1

        if failed_items:
            raise RuntimeError(
                f"Cache cleanup partially failed: "
                f"{deleted_items} items removed, "
                f"{failed_items} items could not be removed."
            )

        return (
            f"Cache cleanup completed successfully. "
            f"{deleted_items} items removed from {cache_directory}."
        )

    def _remove_directory(self, directory: Path) -> None:
        """Remove a directory and its contents safely."""

        for item in directory.iterdir():
            if item.is_dir() and not item.is_symlink():
                self._remove_directory(item)
            else:
                item.unlink()

        directory.rmdir()
