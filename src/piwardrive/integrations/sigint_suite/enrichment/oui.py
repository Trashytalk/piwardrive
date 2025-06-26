"""Vendor lookup helpers using the IEEE OUI registry."""

import csv
import logging
import os
import time
from functools import lru_cache
from typing import Dict, Optional

try:  # pragma: no cover - optional dependency
    from piwardrive.utils import HTTP_SESSION
except Exception:  # pragma: no cover - minimal fallback
    class _DummySession:
        def get(self, *_a, **_k):  # pragma: no cover - simple stub
            raise RuntimeError("HTTP session unavailable")

    HTTP_SESSION = _DummySession()
    import requests  # type: ignore
except Exception:  # pragma: no cover - missing dependency
    requests = None  # type: ignore

if requests is not None:
    HTTP_SESSION = requests.Session()
else:  # pragma: no cover - unit tests stub this out
    HTTP_SESSION = None  # type: ignore

from sigint_suite import paths

# Persist the OUI registry under the main configuration directory
OUI_PATH = paths.OUI_PATH

# Source for the vendor registry
OUI_URL = "https://standards-oui.ieee.org/oui/oui.csv"

# Refresh weekly by default
OUI_MAX_AGE = 7 * 24 * 3600

_OUI_MAP: Dict[str, str] = {}
_OUI_MTIME = 0.0

logger = logging.getLogger(__name__)


def update_oui_file(
    path: str = OUI_PATH,
    url: str = OUI_URL,
    max_age: int = OUI_MAX_AGE,
) -> None:
    """Download the vendor registry if ``path`` is missing or stale."""
    try:
        mtime = os.path.getmtime(path)
        if time.time() - mtime < max_age:
            return
    except FileNotFoundError:
        pass

    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        resp = HTTP_SESSION.get(url, timeout=15)
        resp.raise_for_status()
    except Exception as exc:
        logger.error("OUI registry download failed: %s", exc)
        return

    with open(path, "wb") as fh:
        fh.write(resp.content)


def _load_map(path: str) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    if not os.path.exists(path):
        return mapping
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            assignment = (row.get("Assignment") or "").strip()
            vendor = (row.get("Organization Name") or "").strip()
            if assignment and vendor:
                prefix = assignment.replace("-", ":").upper()
                mapping[prefix] = vendor
    return mapping


def load_oui_map(path: str = OUI_PATH) -> Dict[str, str]:
    """Return a mapping of MAC prefixes to vendor names."""
    global _OUI_MAP, _OUI_MTIME
    update_oui_file(path)
    try:
        mtime = os.path.getmtime(path)
    except FileNotFoundError:
        return {}
    if _OUI_MAP and _OUI_MTIME == mtime:
        return _OUI_MAP
    _OUI_MAP = _load_map(path)
    _OUI_MTIME = mtime
    return _OUI_MAP


def _default_map() -> Dict[str, str]:
    return load_oui_map()


def lookup_vendor(
    bssid: str, oui_map: Optional[Dict[str, str]] = None
) -> Optional[str]:
    """Return vendor name for ``bssid`` if known."""
    if not bssid:
        return None
    bssid = bssid.upper().replace("-", ":")
    parts = bssid.split(":")
    if len(parts) < 3:
        return None
    prefix = ":".join(parts[:3])
    return (oui_map or _default_map()).get(prefix)


@lru_cache(maxsize=1024)
def cached_lookup_vendor(bssid: str) -> Optional[str]:
    """LRU cached wrapper for :func:`lookup_vendor`."""
    return lookup_vendor(bssid)


__all__ = ["load_oui_map", "lookup_vendor", "cached_lookup_vendor", "update_oui_file"]
