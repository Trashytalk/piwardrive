"""System diagnostic helpers for PiWardrive."""

from __future__ import annotations

import asyncio
import cProfile
import gzip
import io
import logging
import os
import pstats
import shutil
import subprocess
import time
from datetime import datetime
from typing import Any, Dict

import psutil

from piwardrive import cloud_export, config, r_integration, utils
from piwardrive.interfaces import DataCollector, SelfTestCollector
from piwardrive.persistence import (
    HealthRecord,
    load_recent_health,
    purge_old_health,
    save_health_record,
    vacuum,
)
from piwardrive.scheduler import PollScheduler
from piwardrive.utils import run_async_task

_PROFILER: cProfile.Profile | None = None
_LAST_NETWORK_OK: float | None = None


def _upload_to_cloud(path: str) -> None:
    """Upload ``path`` to configured cloud storage if enabled."""
    cfg = config.AppConfig.load()
    if not cfg.cloud_bucket:
        return
    key = os.path.join(cfg.cloud_prefix.strip("/"), os.path.basename(path))
    try:
        cloud_export.upload_to_s3(
            path, cfg.cloud_bucket, key, cfg.cloud_profile or None
        )
    except Exception as exc:  # pragma: no cover - upload errors
        logging.exception("Cloud upload failed: %s", exc)


def generate_system_report() -> Dict[str, Any]:
    """Return a dictionary with basic system metrics."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "cpu_temp": utils.get_cpu_temp(),
        "cpu_percent": psutil.cpu_percent(interval=None),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
        "ssd_smart": utils.get_smart_status("/mnt/ssd"),
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
    _upload_to_cloud(f"{tmp}.gz")


async def rotate_log_async(path: str, max_files: int = 3) -> None:
    """Asynchronously rotate and gzip ``path`` using ``aiofiles``."""
    if not os.path.exists(path):
        return

    try:
        import aiofiles  # type: ignore
    except Exception:  # pragma: no cover - optional dependency
        await asyncio.to_thread(rotate_log, path, max_files)
        return

    for ext in (".gz", ""):
        old = f"{path}.{max_files}{ext}"
        if os.path.exists(old):
            os.remove(old)

    for i in range(max_files - 1, 0, -1):
        src_gz = f"{path}.{i}.gz"
        dst_gz = f"{path}.{i+1}.gz"
        if os.path.exists(src_gz):
            os.rename(src_gz, dst_gz)
            continue
        src = f"{path}.{i}"
        if os.path.exists(src):
            os.rename(src, dst_gz)

    tmp = f"{path}.1"
    os.rename(path, tmp)
    async with aiofiles.open(tmp, "rb") as f_in:
        data = await f_in.read()
    async with aiofiles.open(f"{tmp}.gz", "wb") as f_out:
        await f_out.write(gzip.compress(data))
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
    stats = pstats.Stats(_PROFILER, stream=s).strip_dirs().sort_stats("cumulative")
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


def get_profile_metrics() -> Dict[str, float] | None:
    """Return simple metrics from the active profiler."""
    if _PROFILER is None:
        return None
    stats = _PROFILER.getstats()
    total = sum(rec.totaltime for rec in stats)
    return {"calls": len(stats), "cumtime": total}


def run_network_test(host: str = "8.8.8.8", cache_seconds: float = 30.0) -> bool:
    """Ping ``host`` once and return True if reachable.

    If the previous successful check occurred within ``cache_seconds`` the
    ping call is skipped and ``True`` is returned immediately.
    """
    global _LAST_NETWORK_OK
    now = time.time()
    if _LAST_NETWORK_OK is not None and now - _LAST_NETWORK_OK < cache_seconds:
        return True
    try:
        subprocess.run(["ping", "-c", "1", host], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        return False
    _LAST_NETWORK_OK = now
    return True


def get_interface_status() -> Dict[str, bool]:
    """Return mapping of network interface names to ``isup`` booleans."""
    return {name: stats.isup for name, stats in psutil.net_if_stats().items()}


def list_usb_devices() -> list[str]:
    """Return lines of ``lsusb`` output as a list."""
    try:
        proc = subprocess.run(["lsusb"], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError:
        return []
    return proc.stdout.strip().splitlines()


def get_service_statuses(
    services: tuple[str, ...] | list[str] | None = None,
) -> Dict[str, bool]:
    """Return mapping of service names to their ``systemd`` active state."""
    if services is None:
        services = ("kismet", "bettercap", "gpsd")
    return {svc: utils.service_status(svc) for svc in services}


def self_test() -> Dict[str, Any]:
    """Run a few checks and return their results."""
    return {
        "system": generate_system_report(),
        "network_ok": run_network_test(),
        "interfaces": get_interface_status(),
        "usb": list_usb_devices(),
        "services": get_service_statuses(),
    }


class HealthMonitor:
    """Background poller for metric collectors."""

    def __init__(
        self,
        scheduler: "PollScheduler",
        interval: float = 10.0,
        collector: DataCollector | None = None,
        daily_summary: bool = False,
    ) -> None:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())
        self._scheduler = scheduler
        self._collector: DataCollector = collector or SelfTestCollector()
        self.data: Dict[str, Any] | None = None
        self._event = "health_monitor"
        scheduler.schedule(
            self._event,
            lambda dt: run_async_task(self._poll()),
            interval,
        )
        self._summary_event = "health_summary"
        if daily_summary:
            scheduler.schedule(
                self._summary_event,
                lambda dt: run_async_task(self._run_summary()),
                86400,
            )
        self._export_event = "health_export"
        if config.HEALTH_EXPORT_INTERVAL > 0:
            scheduler.schedule(
                self._export_event,
                lambda dt: run_async_task(self._run_export()),
                config.HEALTH_EXPORT_INTERVAL * 3600,
            )
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
            await purge_old_health(30)
            await vacuum()
        except Exception as exc:  # pragma: no cover - diagnostics best-effort
            logging.exception("HealthMonitor poll failed: %s", exc)

    async def _run_summary(self) -> None:
        import csv
        import json
        from dataclasses import asdict

        try:
            records = await load_recent_health(10000)
        except Exception as exc:  # pragma: no cover - best-effort
            logging.exception("HealthMonitor load records failed: %s", exc)
            return

        if not records:
            return

        cfg = config.AppConfig.load()
        os.makedirs(cfg.reports_dir, exist_ok=True)
        date = datetime.now().strftime("%Y%m%d")
        csv_path = os.path.join(cfg.reports_dir, f"health_{date}.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh,
                fieldnames=[
                    "timestamp",
                    "cpu_temp",
                    "cpu_percent",
                    "memory_percent",
                    "disk_percent",
                ],
            )
            writer.writeheader()
            writer.writerows(asdict(r) for r in records)

        plot_path = os.path.join(cfg.reports_dir, f"health_{date}.png")

        try:
            result = await asyncio.to_thread(
                r_integration.health_summary, csv_path, plot_path
            )
        except Exception as exc:  # pragma: no cover - optional
            logging.exception("HealthMonitor summary failed: %s", exc)
            return

        json_path = os.path.join(cfg.reports_dir, f"health_{date}.json")
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(result, fh)

    async def _run_export(self) -> None:
        import piwardrive.scripts.health_export as health_export

        try:
            cfg = config.AppConfig.load()
            os.makedirs(cfg.health_export_dir, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            path = os.path.join(cfg.health_export_dir, f"health_{ts}.json")
            await asyncio.to_thread(
                health_export.main,
                [path, "--format", "json", "--limit", "10000"],
            )
            if cfg.compress_health_exports:
                with open(path, "rb") as fin, gzip.open(path + ".gz", "wb") as fout:
                    shutil.copyfileobj(fin, fout)
                os.remove(path)
                path += ".gz"
            await asyncio.to_thread(self._cleanup_exports)
            logging.info("Exported health data to %s", path)
            await asyncio.to_thread(_upload_to_cloud, path)
        except Exception as exc:  # pragma: no cover - best-effort
            logging.exception("HealthMonitor export failed: %s", exc)

    def _cleanup_exports(self) -> None:
        cfg = config.AppConfig.load()
        if cfg.health_export_retention <= 0:
            return
        cutoff = datetime.now().timestamp() - cfg.health_export_retention * 86400
        for fname in os.listdir(cfg.health_export_dir):
            fpath = os.path.join(cfg.health_export_dir, fname)
            try:
                if os.path.isfile(fpath) and os.path.getmtime(fpath) < cutoff:
                    os.remove(fpath)
            except Exception:  # pragma: no cover - cleanup best effort
                logging.exception("Failed to remove old export %s", fpath)

    def stop(self) -> None:
        """Cancel the periodic health export task."""
        self._scheduler.cancel(self._event)


__all__ = [
    "generate_system_report",
    "rotate_log",
    "start_profiling",
    "stop_profiling",
    "get_profile_metrics",
    "run_network_test",
    "get_interface_status",
    "list_usb_devices",
    "get_service_statuses",
    "self_test",
    "HealthMonitor",
]
