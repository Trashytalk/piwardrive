"""System diagnostic helpers for PiWardrive.

This module provides comprehensive system diagnostic functionality including
performance profiling, resource monitoring, health checks, and automated
diagnostics for the PiWardrive system.
"""

from __future__ import annotations

import asyncio
import cProfile
import gzip
import io
import os
import pstats
import shutil
import subprocess
import time
from datetime import datetime
from typing import Any, Dict
from uuid import uuid4

import psutil

from piwardrive import cloud_export, config, r_integration, utils
from piwardrive.database_service import db_service
from piwardrive.exceptions import PiWardriveError, ServiceError
from piwardrive.interfaces import DataCollector, SelfTestCollector
from piwardrive.logging.structured_logger import get_logger
from piwardrive.mqtt import MQTTClient
from piwardrive.persistence import HealthRecord
from piwardrive.scheduler import PollScheduler
from piwardrive.utils import run_async_task

logger = get_logger(__name__).logger

_PROFILER: cProfile.Profile | None = None
_LAST_NETWORK_OK: float | None = None

DEFAULT_LOG_ARCHIVES = 3
NETWORK_TEST_CACHE_SECONDS = 30.0
HEALTH_MONITOR_INTERVAL = 10.0


def _upload_to_cloud(path: str) -> None:
    """Upload ``path`` to configured cloud storage if enabled."""
    cfg = config.AppConfig.load()
    if not cfg.cloud_bucket:
        return
    key = os.path.join(cfg.cloud_prefix.strip("/"), os.path.basename(path))
    cid = str(uuid4())
    try:
        cloud_export.upload_to_s3(
            path, cfg.cloud_bucket, key, cfg.cloud_profile or None
        )
    except Exception as exc:  # pragma: no cover - upload errors
        logger.error(
            "Cloud upload failed",
            exc_info=exc,
            extra={"correlation_id": cid, "path": path},
        )
        raise ServiceError(f"Failed to upload {path}") from exc


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


def rotate_log(path: str, max_files: int = DEFAULT_LOG_ARCHIVES) -> None:
    """Rotate and gzip ``path`` keeping ``max_files`` archives."""
    if max_files < 1:
        raise ValueError(f"max_files must be >= 1, got {max_files}")
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


async def rotate_log_async(path: str, max_files: int = DEFAULT_LOG_ARCHIVES) -> None:
    """Asynchronously rotate and gzip ``path`` using ``aiofiles``."""
    if max_files < 1:
        raise ValueError(f"max_files must be >= 1, got {max_files}")
    if not os.path.exists(path):
        return

    try:
        import aiofiles
    except ImportError:  # pragma: no cover - optional dependency
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
        except ImportError as exc:  # pragma: no cover - optional
            logger.warning("pyprof2calltree not available: %s", exc)
        else:
            try:
                pyprof2calltree.convert(stats, path)
            except Exception as exc:  # pragma: no cover - optional
                logger.error("Failed to export callgrind data", exc_info=exc)
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


def run_network_test(
    host: str = "8.8.8.8", cache_seconds: float = NETWORK_TEST_CACHE_SECONDS
) -> bool:
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
    services = get_service_statuses()

    cfg = config.AppConfig.load()
    restart = set(cfg.restart_services)
    for name, active in services.items():
        if not active and name in restart:
            utils.run_service_cmd(name, "restart")

    return {
        "system": generate_system_report(),
        "network_ok": run_network_test(),
        "interfaces": get_interface_status(),
        "usb": list_usb_devices(),
        "services": services,
    }


class HealthMonitor:
    """Background poller for metric collectors."""

    def __init__(
        self,
        scheduler: "PollScheduler",
        interval: float = HEALTH_MONITOR_INTERVAL,
        collector: DataCollector | None = None,
        daily_summary: bool = False,
        mqtt_client: "MQTTClient | None" = None,
    ) -> None:
        """Initialize health monitor with scheduler and configuration.

        Args:
            scheduler: The poll scheduler to use for monitoring.
            interval: Monitoring interval in seconds.
            collector: Optional custom data collector.
            daily_summary: Whether to generate daily summaries.
            mqtt_client: Optional MQTT client for notifications.
        """
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())
        self._scheduler = scheduler
        self._collector: DataCollector = collector or SelfTestCollector()
        self._mqtt = mqtt_client
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
        cid = str(uuid4())
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
            await db_service.save_health_record(rec)
            try:
                from piwardrive import analysis

                analysis.process_new_record(rec)
            except PiWardriveError as exc:
                logger.error(
                    "ML processing failed",
                    exc_info=exc,
                    extra={"correlation_id": cid},
                )
            except Exception as exc:  # pragma: no cover - optional hooks
                logger.exception(
                    "ML processing failed: %s", exc, extra={"correlation_id": cid}
                )
            await db_service.purge_old_health(30)
            await db_service.vacuum()
            if self._mqtt:
                try:
                    self._mqtt.publish(self.data or {})
                except Exception as exc:
                    logger.exception(
                        "MQTT publish failed",
                        exc_info=exc,
                        extra={"correlation_id": cid},
                    )
        except PiWardriveError as exc:  # pragma: no cover - diagnostics best-effort
            logger.error(
                "HealthMonitor poll failed", exc_info=exc, extra={"correlation_id": cid}
            )
        except Exception as exc:  # pragma: no cover - diagnostics best-effort
            logger.exception(
                "HealthMonitor poll failed: %s", exc, extra={"correlation_id": cid}
            )

    async def _run_summary(self) -> None:
        import csv
        import json
        from dataclasses import asdict

        cid = str(uuid4())
        try:
            records = await db_service.load_recent_health(10000)
        except PiWardriveError as exc:  # pragma: no cover - best-effort
            logger.error(
                "HealthMonitor load records failed",
                exc_info=exc,
                extra={"correlation_id": cid},
            )
            return
        except Exception as exc:  # pragma: no cover - best-effort
            logger.exception(
                "HealthMonitor load records failed: %s",
                exc,
                extra={"correlation_id": cid},
            )
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
        except PiWardriveError as exc:  # pragma: no cover - optional
            logger.error(
                "HealthMonitor summary failed",
                exc_info=exc,
                extra={"correlation_id": cid},
            )
            return
        except Exception as exc:  # pragma: no cover - optional
            logger.exception(
                "HealthMonitor summary failed: %s",
                exc,
                extra={"correlation_id": cid},
            )
            return

        json_path = os.path.join(cfg.reports_dir, f"health_{date}.json")
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(result, fh)

    async def _run_export(self) -> None:
        import piwardrive.scripts.health_export as health_export

        cid = str(uuid4())
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
            logger.info(
                "Exported health data to %s", path, extra={"correlation_id": cid}
            )
            await asyncio.to_thread(_upload_to_cloud, path)
        except PiWardriveError as exc:  # pragma: no cover - best-effort
            logger.error(
                "HealthMonitor export failed",
                exc_info=exc,
                extra={"correlation_id": cid},
            )
        except Exception as exc:  # pragma: no cover - best-effort
            logger.exception(
                "HealthMonitor export failed: %s", exc, extra={"correlation_id": cid}
            )

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
            except Exception as exc:  # pragma: no cover - cleanup best effort
                logger.exception("Failed to remove old export %s", fpath, exc_info=exc)

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
