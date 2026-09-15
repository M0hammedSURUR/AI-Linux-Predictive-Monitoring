from dataclasses import dataclass
import json
from pathlib import Path
import subprocess


@dataclass
class ServiceStatus:
    """Represent the current status of a systemd service."""

    service_name: str
    status: str
    description: str


class SystemdServiceMonitor:
    """Monitor selected Linux systemd services."""

    def __init__(self, services: list[str]):
        self.services = services

    @classmethod
    def from_config(
        cls,
        config_path: Path,
    ) -> "SystemdServiceMonitor":
        """Create a monitor using services from a JSON configuration."""

        with config_path.open("r", encoding="utf-8") as file:
            config = json.load(file)

        services = config.get("services", [])

        if not isinstance(services, list):
            raise ValueError(
                "The 'services' configuration must be a list."
            )

        return cls(services)

    def check_service(self, service_name: str) -> ServiceStatus:
        """Check the current status of one systemd service."""

        try:
            result = subprocess.run(
                [
                    "systemctl",
                    "is-active",
                    service_name,
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            status = result.stdout.strip() or "unknown"

            description_result = subprocess.run(
                [
                    "systemctl",
                    "show",
                    service_name,
                    "--property=Description",
                    "--value",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            description = (
                description_result.stdout.strip()
                or "No description available"
            )

            return ServiceStatus(
                service_name=service_name,
                status=status,
                description=description,
            )

        except OSError as exc:
            return ServiceStatus(
                service_name=service_name,
                status="error",
                description=str(exc),
            )

    def check_all(self) -> list[ServiceStatus]:
        """Check all configured services."""

        return [
            self.check_service(service)
            for service in self.services
        ]
