"""System diagnostic helpers for PiWardrive."""

from __future__ import annotations

import os
import subprocess
from datetime import datetime

import psutil


def generate_system_report() -> dict:
    """Return a dictionary with basic system metrics."""
    return {
        "timestamp": datetime.now().isoformat(),
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


def self_test() -> dict:
    """Run a few checks and return their results."""
    return {
        'system': generate_system_report(),
        'network_ok': run_network_test(),
    }
