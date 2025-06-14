"""System diagnostic helpers for PiWardrive."""

from __future__ import annotations

import os
import subprocess
from datetime import datetime

import psutil
import logging

import utils
from scheduler import PollScheduler

def generate_system_report() -> dict:
    """Return a dictionary with basic system metrics."""
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_temp": utils.get_cpu_temp(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
    }


def rotate_log(path: str, max_files: int = 3) -> None:
    """Simple log rotation renaming path -> path.1 etc."""
    if not os.path.exists(path):
        return
    for i in range(max_files, 0, -1):
        src = f"{path}.{i-1}" if i > 1 else path
        dst = f"{path}.{i}"
        if os.path.exists(src):
            os.rename(src, dst)


def run_network_test(host: str = '8.8.8.8') -> bool:
    """Ping ``host`` once and return True if reachable."""
    proc = subprocess.run(['ping', '-c', '1', host], capture_output=True)
    return proc.returncode == 0

def get_interface_status() -> dict:
    """Return mapping of network interface names to ``isup`` booleans."""
    return {name: stats.isup for name, stats in psutil.net_if_stats().items()}


def list_usb_devices() -> list[str]:
    """Return lines of ``lsusb`` output as a list."""
    proc = subprocess.run(['lsusb'], capture_output=True, text=True)
    if proc.returncode == 0:
        return proc.stdout.strip().splitlines()
    return []


def get_service_statuses(services: tuple[str, ...] | list[str] | None = None) -> dict:
    """Return mapping of service names to their ``systemd`` active state."""
    if services is None:
        services = ('kismet', 'bettercap', 'gpsd')
    return {svc: utils.service_status(svc) for svc in services}



def self_test() -> dict:
    """Run a few checks and return their results."""
    return {
        'system': generate_system_report(),
        'network_ok': run_network_test(),
        'interfaces': get_interface_status(),
        'usb': list_usb_devices(),
        'services': get_service_statuses(),
    }


class HealthMonitor:
    """Background poller for :func:`self_test` results."""

    def __init__(self, scheduler: 'PollScheduler', interval: float = 10.0) -> None:
        self._scheduler = scheduler
        self._interval = interval
        self.data: dict | None = None
        self._event = "health_monitor"
        scheduler.schedule(self._event, lambda dt: self._poll(), interval)
        self._poll()

    def _poll(self) -> None:
        try:
            self.data = self_test()
        except Exception as exc:  # pragma: no cover - diagnostics best-effort
            logging.exception("HealthMonitor poll failed: %s", exc)

    def stop(self) -> None:
        self._scheduler.cancel(self._event)
