from unittest.mock import patch

from src.service_monitor.systemd_monitor import (
    ServiceStatus,
    SystemdServiceMonitor,
)


def test_check_service_returns_active_status():
    monitor = SystemdServiceMonitor(["cron.service"])

    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            type(
                "Result",
                (),
                {
                    "stdout": "active\n",
                    "returncode": 0,
                },
            )(),
            type(
                "Result",
                (),
                {
                    "stdout": "Regular background program processing daemon\n",
                    "returncode": 0,
                },
            )(),
        ]

        result = monitor.check_service("cron.service")

    assert isinstance(result, ServiceStatus)
    assert result.service_name == "cron.service"
    assert result.status == "active"
    assert result.description == (
        "Regular background program processing daemon"
    )


def test_check_all_returns_all_services():
    monitor = SystemdServiceMonitor(
        [
            "cron.service",
            "bluetooth.service",
        ]
    )

    with patch.object(
        monitor,
        "check_service",
        side_effect=[
            ServiceStatus(
                service_name="cron.service",
                status="active",
                description="Cron",
            ),
            ServiceStatus(
                service_name="bluetooth.service",
                status="inactive",
                description="Bluetooth",
            ),
        ],
    ):
        results = monitor.check_all()

    assert len(results) == 2
    assert results[0].service_name == "cron.service"
    assert results[1].service_name == "bluetooth.service"


def test_from_config_loads_services(tmp_path):
    config_file = tmp_path / "services.json"

    config_file.write_text(
        '{"services": ["cron.service", "cups.service"]}',
        encoding="utf-8",
    )

    monitor = SystemdServiceMonitor.from_config(config_file)

    assert monitor.services == [
        "cron.service",
        "cups.service",
    ]
