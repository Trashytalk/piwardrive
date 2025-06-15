"""System diagnostic helpers for PiWardrive."""

from __future__ import annotations

import os
import subprocess
from datetime import datetime
import cProfile
import pstats
import io
import gzip
import shutil

import psutil
import logging
import asyncio

import utils
from scheduler import PollScheduler
from interfaces import DataCollector, SelfTestCollector
from persistence import HealthRecord, save_health_record
from utils import run_async_task

_PROFILER: cProfile.Profile | None = None


def generate_system_report() -> dict:
    """Return a dictionary with basic system metrics."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "cpu_temp": utils.get_cpu_temp(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "ssd_smart": utils.get_smart_status('/mnt/ssd'),
    }
    metrics = get_profile_metrics()
    if metrics:
        report["profile"] = metrics
    return report


def rotate_log(path: str, max_files: int = 3) -> None:
    """Rotate and gzip ``path`` keeping ``max_files`` archives."""
    if not os.path.exists(path):
        return

    # Drop the oldest archive (both compressed or previous uncompressed forms)
    for ext in (".gz", ""):
        old = f"{path}.{max_files}{ext}"
        if os.path.exists(old):
            os.remove(old)

    # Shift existing archives up by one index
    for i in range(max_files - 1, 0, -1):
        src_gz = f"{path}.{i}.gz"
        dst_gz = f"{path}.{i+1}.gz"
        if os.path.exists(src_gz):
            os.rename(src_gz, dst_gz)
            continue
        src = f"{path}.{i}"
        if os.path.exists(src):
            os.rename(src, dst_gz)

    # Compress the current log as .1.gz
    tmp = f"{path}.1"
    os.rename(path, tmp)
    with open(tmp, "rb") as f_in, gzip.open(f"{tmp}.gz", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(tmp)


def start_profiling() -> None:
    """Enable global cProfile collection."""
    global _PROFILER
    if _PROFILER is None:
        _PROFILER = cProfile.Profile()
        _PROFILER.enable()


def stop_profiling() -> str | None:
    """Disable profiling and return a formatted stats string."""
    global _PROFILER
    if _PROFILER is None:
        return None
    _PROFILER.disable()
    s = io.StringIO()
    stats = (
        pstats.Stats(_PROFILER, stream=s)
        .strip_dirs()
        .sort_stats("cumulative")
    )
    stats.print_stats(10)
    path = os.getenv("PW_PROFILE_CALLGRIND")
    if path:
        try:
            import pyprof2calltree

            pyprof2calltree.convert(stats, path)
        except Exception as exc:  # pragma: no cover - optional
            logging.exception("Failed to export callgrind data: %s", exc)
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write("")
            except Exception:

                pass
    _PROFILER = None
    return s.getvalue()


def get_profile_metrics() -> dict | None:
    """Return simple metrics from the active profiler."""
    if _PROFILER is None:
        return None
    stats = _PROFILER.getstats()
    total = sum(rec.totaltime for rec in stats)
    return {"calls": len(stats), "cumtime": total}


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
    """Background poller for metric collectors."""

    def __init__(
        self,
        scheduler: 'PollScheduler',
        interval: float = 10.0,
        collector: DataCollector | None = None,
    ) -> None:
        self._scheduler = scheduler
        self._interval = interval
        self._collector: DataCollector = collector or SelfTestCollector()
        self.data: dict | None = None
        self._event = "health_monitor"
        scheduler.schedule(self._event, lambda dt: run_async_task(self._poll()), interval)
        asyncio.run(self._poll())

    async def _poll(self) -> None:
        try:
            self.data = await asyncio.to_thread(self._collector.collect)
            system = self.data.get("system", {}) if self.data else {}
            rec = HealthRecord(
                timestamp=system.get("timestamp", datetime.now().isoformat()),
                cpu_temp=system.get("cpu_temp"),
                cpu_percent=system.get("cpu_percent", 0.0),
                memory_percent=system.get("memory_percent", 0.0),
                disk_percent=system.get("disk_percent", 0.0),
            )
            await save_health_record(rec)
        except Exception as exc:  # pragma: no cover - diagnostics best-effort
            logging.exception("HealthMonitor poll failed: %s", exc)

    def stop(self) -> None:
        self._scheduler.cancel(self._event)
