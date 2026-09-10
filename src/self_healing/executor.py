from pathlib import Path  # NEW

from src.self_healing.models import HealingAction


class SelfHealingExecutor:
    """Executes only predefined, approved healing actions."""

    # NEW: Whitelist of actions that the executor is allowed to perform
    ALLOWED_ACTIONS = {
        "clear_cache",
        "restart_service",
    }

    # NEW: Restrict cache cleanup to the current user's cache directory
    CACHE_DIRECTORY = Path.home() / ".cache"

    # NEW: Maximum time allowed for a healing operation
    EXECUTION_TIMEOUT_SECONDS = 10

    def execute(self, action: HealingAction) -> str:
        """Execute an approved healing action."""

        # Only approved actions can be executed
        if action.status != "approved":
            raise ValueError(
                "Only approved healing actions can be executed."
            )

        # Block actions that are not explicitly whitelisted
        if action.action not in self.ALLOWED_ACTIONS:
            raise ValueError(
                f"Action '{action.action}' is not allowed."
            )

        # NEW: Execute the real cache-clearing action
        if action.action == "clear_cache":
            return self._clear_cache()

        # NEW: Keep service restart disabled until its real
        # implementation is safely designed and tested.
        if action.action == "restart_service":
            raise ValueError(
                "Real service restart is not implemented yet."
            )

        # Defensive fallback
        raise ValueError(
            f"Unsupported healing action: {action.action}"
        )

    # NEW: Safely clear only the contents of ~/.cache
    def _clear_cache(self) -> str:
        """Remove cache contents without deleting the cache directory."""

        cache_directory = self.CACHE_DIRECTORY.resolve()

        # NEW: Safety check — the target must exist and be a directory
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

        # NEW: Delete only direct children of ~/.cache
        for item in cache_directory.iterdir():
            try:
                if item.is_dir() and not item.is_symlink():
                    self._remove_directory(item)
                else:
                    item.unlink()

                deleted_items += 1

            except OSError:
                failed_items += 1

        # NEW: Report the result without exposing arbitrary commands
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

    # NEW: Recursively remove a directory using Python filesystem APIs
    def _remove_directory(self, directory: Path) -> None:
        """Remove a directory and its contents safely."""

        for item in directory.iterdir():
            if item.is_dir() and not item.is_symlink():
                self._remove_directory(item)
            else:
                item.unlink()

        directory.rmdir()
