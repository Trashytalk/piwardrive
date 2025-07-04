"""Public persistence helpers for :mod:`piwardrive`.

This module re-exports the database utilities from
:mod:`piwardrive.core.persistence`. Importing from this location keeps
database-related helpers in a consistent namespace while allowing the core
implementation to reside in the ``core`` package.
"""

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from . import config
from .core.persistence import *  # noqa: F401,F403,F405
from .core.persistence import (
    ScanSession,
    _acquire_conn,
    _db_path,
    _get_conn,
    _release_conn,
    backup_database,
    get_db_metrics,
    get_scan_session,
    iter_scan_sessions,
    load_daily_detection_stats,
    load_network_coverage_grid,
    refresh_daily_detection_stats,
    refresh_network_coverage_grid,
    save_scan_session,
    shutdown_pool,
)


@dataclass
class FingerprintInfo:
    """Metadata about a captured fingerprint."""

    environment: str
    source: str
    record_count: int
    created_at: str | None = None


async def save_fingerprint_info(info: FingerprintInfo) -> None:
    """Append ``info`` to ``fingerprints.json`` under ``CONFIG_DIR``."""
    path = Path(config.CONFIG_DIR) / "fingerprints.json"
    try:
        data = json.loads(path.read_text()) if path.exists() else []
    except Exception:
        data = []
    data.append(asdict(info))
    path.write_text(json.dumps(data))


async def load_fingerprint_info() -> list[FingerprintInfo]:
    """Return stored fingerprint metadata."""
    path = Path(config.CONFIG_DIR) / "fingerprints.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text())
    except Exception:
        return []
    return [FingerprintInfo(**d) for d in data]


async def create_user(*_a, **_k) -> None:
    """Stub for ``service`` imports."""


async def get_user(*_a, **_k):
    """Stub returning ``None`` for ``service`` imports."""
    return None


async def get_user_by_token(*_a, **_k):
    """Stub returning ``None`` for ``service`` imports."""
    return None


async def save_user(*_a, **_k) -> None:
    """Stub for ``service`` imports."""


async def update_user_token(*_a, **_k) -> None:
    """Stub for ``service`` imports."""


__all__ = [  # noqa: F405
    *globals().get("__all__", []),
    "_db_path",
    "_get_conn",
    "_acquire_conn",
    "_release_conn",
    "shutdown_pool",
    "backup_database",
    "get_db_metrics",
    "FingerprintInfo",
    "save_fingerprint_info",
    "load_fingerprint_info",
    "create_user",
    "get_user",
    "get_user_by_token",
    "save_user",
    "update_user_token",
    "ScanSession",
    "save_scan_session",
    "get_scan_session",
    "iter_scan_sessions",
    "save_gps_tracks",
    "save_suspicious_activities",
    "count_suspicious_activities",
    "load_recent_suspicious",
    "save_network_analytics",
    "load_network_analytics",
    "refresh_daily_detection_stats",
    "refresh_network_coverage_grid",
    "load_daily_detection_stats",
    "load_network_coverage_grid",
]
