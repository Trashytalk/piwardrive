import asyncio
import gzip
import logging
import logging.handlers
import os
import shutil
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Dict, List, Optional

from prometheus_client import Counter, Gauge, Histogram

from .scheduler import RotationScheduler
from .storage import LogArchiveManager, LogRetentionManager

# Metrics
ROTATION_COUNTER = Counter(
    "log_rotation_total", "Total log rotations", ["policy", "status"]
)
COMPRESSION_TIME = Histogram(
    "log_compression_duration_seconds", "Time spent compressing logs"
)
ARCHIVE_SIZE = Gauge("log_archive_size_bytes", "Size of archived logs", ["backend"])


@dataclass
class RotationPolicy:
    """Configuration for log rotation policy."""

    name: str
    max_size: Optional[int] = None  # bytes
    max_age: Optional[timedelta] = None
    max_files: int = 10
    compression: bool = True
    compression_level: int = 6
    archive_to: Optional[str] = None
    retention_days: int = 30
    min_free_space: Optional[int] = None  # bytes


class LogRotationManager:
    """Manages log rotation across multiple log files and policies."""

    def __init__(self, config: Dict[str, any]):
        self.config = config
        self.policies: Dict[str, RotationPolicy] = {}
        self.handlers: Dict[str, "SmartRotatingHandler"] = {}
        self.scheduler = RotationScheduler()
        self.archive_manager = LogArchiveManager(config)
        self.retention_manager = LogRetentionManager(config)
        self._load_policies()
        self.scheduler.schedule_retention_cleanup(self.retention_manager)

    def _parse_timedelta(self, value: Optional[str]) -> Optional[timedelta]:
        if not value:
            return None
        try:
            if value.endswith("h"):
                return timedelta(hours=int(value[:-1]))
            if value.endswith("d"):
                return timedelta(days=int(value[:-1]))
            return timedelta(seconds=int(value))
        except Exception:
            return None

    def _load_policies(self):
        """Load rotation policies from configuration."""
        for policy_name, policy_config in self.config.get("policies", {}).items():
            self.policies[policy_name] = RotationPolicy(
                name=policy_name,
                max_size=policy_config.get("max_size"),
                max_age=self._parse_timedelta(policy_config.get("max_age")),
                max_files=policy_config.get("max_files", 10),
                compression=policy_config.get("compression", True),
                compression_level=policy_config.get("compression_level", 6),
                archive_to=policy_config.get("archive_to"),
                retention_days=policy_config.get("retention_days", 30),
                min_free_space=policy_config.get("min_free_space"),
            )

    def create_handler(self, log_file: str, policy_name: str) -> "SmartRotatingHandler":
        """Create a rotating handler with specified policy."""
        if policy_name not in self.policies:
            raise ValueError(f"Unknown rotation policy: {policy_name}")

        policy = self.policies[policy_name]
        handler = SmartRotatingHandler(log_file, policy, self)
        self.handlers[log_file] = handler

        # Schedule rotation checks
        self.scheduler.schedule_rotation_check(handler)

        return handler

    def force_rotation(self, log_file: str):
        """Force rotation of specific log file."""
        if log_file in self.handlers:
            self.handlers[log_file].doRollover()


class SmartRotatingHandler(logging.handlers.BaseRotatingHandler):
    """Advanced rotating handler with multiple rotation strategies."""

    def __init__(
        self, filename: str, policy: RotationPolicy, manager: LogRotationManager
    ):
        super().__init__(filename, "a", encoding="utf-8")
        self.policy = policy
        self.manager = manager
        self.rotation_lock = threading.RLock()
        self.last_rollover = datetime.utcnow()
        self._setup_rotation_conditions()

    def _setup_rotation_conditions(self):
        """Setup conditions that trigger rotation."""
        self.rotation_conditions: List[Callable[[], bool]] = []

        if self.policy.max_size:
            self.rotation_conditions.append(self._check_size_limit)

        if self.policy.max_age:
            self.rotation_conditions.append(self._check_age_limit)

        if self.policy.min_free_space:
            self.rotation_conditions.append(self._check_free_space)

    def shouldRollover(
        self, record: Optional[logging.LogRecord]
    ) -> bool:  # type: ignore[override]
        """Check if log should be rotated."""
        with self.rotation_lock:
            return any(condition() for condition in self.rotation_conditions)

    def doRollover(self):
        """Perform log rotation with compression and archival."""
        with self.rotation_lock:
            ROTATION_COUNTER.labels(self.policy.name, "start").inc()
            if self.stream:
                self.stream.close()
                self.stream = None

            rotated_filename = self._get_rotated_filename()

            if os.path.exists(self.baseFilename):
                os.rename(self.baseFilename, rotated_filename)

            if self.policy.compression:
                start = time.perf_counter()
                compressed_filename = self._compress_log(rotated_filename)
                COMPRESSION_TIME.observe(time.perf_counter() - start)
                os.remove(rotated_filename)
                rotated_filename = compressed_filename

            if self.policy.archive_to:
                self._archive_log(rotated_filename)

            self._cleanup_old_files()
            self.last_rollover = datetime.utcnow()
            self.stream = self._open()
            ROTATION_COUNTER.labels(self.policy.name, "success").inc()

    # ------------------------------------------------------------
    # Rotation condition checks
    def _check_size_limit(self) -> bool:
        if not self.policy.max_size:
            return False
        try:
            return os.path.getsize(self.baseFilename) >= self.policy.max_size
        except FileNotFoundError:
            return False

    def _check_age_limit(self) -> bool:
        if not self.policy.max_age:
            return False
        return datetime.utcnow() - self.last_rollover >= self.policy.max_age

    def _check_free_space(self) -> bool:
        if not self.policy.min_free_space:
            return False
        stat = shutil.disk_usage(os.path.dirname(self.baseFilename))
        return stat.free < self.policy.min_free_space

    # ------------------------------------------------------------
    # Helper methods
    def _get_rotated_filename(self) -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"{self.baseFilename}.{timestamp}"

    def _compress_log(self, filename: str) -> str:
        """Compress log file using gzip."""
        compressed_filename = f"{filename}.gz"
        try:
            with (
                open(filename, "rb") as f_in,
                gzip.open(
                    compressed_filename,
                    "wb",
                    compresslevel=self.policy.compression_level,
                ) as f_out,
            ):
                shutil.copyfileobj(f_in, f_out)
        except OSError as exc:
            logging.error("Failed to compress %s: %s", filename, exc)
            raise
        return compressed_filename

    def _archive_log(self, filename: str) -> None:
        backend = self.manager.archive_manager
        loop = asyncio.get_event_loop()
        try:
            fut = backend.archive_log(filename, self.policy.archive_to or "")
            size = os.path.getsize(filename)
            ARCHIVE_SIZE.labels(self.policy.archive_to).set(size)
            loop.run_until_complete(fut)
        except Exception as exc:
            logging.error("Failed to archive %s: %s", filename, exc)

    def _compress_old_files(self):
        if not self.policy.compression:
            return
        for path in Path(self.baseFilename).parent.glob(
            f"{Path(self.baseFilename).name}.*"
        ):
            if (
                path.suffix != ".gz"
                and path.is_file()
                and not path.name.endswith(".log")
            ):
                try:
                    self._compress_log(str(path))
                    path.unlink()
                except Exception as exc:
                    logging.error("Failed to compress old log %s: %s", path, exc)

    def _cleanup_old_files(self):
        directory = Path(self.baseFilename).parent
        pattern = f"{Path(self.baseFilename).name}.*"
        files = sorted(
            directory.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True
        )
        for old_file in files[self.policy.max_files :]:
            try:
                old_file.unlink()
            except Exception as exc:
                logging.error("Failed to remove old log %s: %s", old_file, exc)
