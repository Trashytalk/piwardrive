"""Vendor lookup helpers using the IEEE OUI registry."""

import csv
import os
import time
from typing import Dict, Optional

import requests

from sigint_suite import paths

# Persist the OUI registry under the main configuration directory
OUI_PATH = paths.OUI_PATH

# Source for the vendor registry
OUI_URL = "https://standards-oui.ieee.org/oui/oui.csv"

# Refresh weekly by default
OUI_MAX_AGE = 7 * 24 * 3600

_OUI_MAP: Dict[str, str] = {}
_OUI_MTIME = 0.0


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
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except Exception:
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
    bssid = bssid.upper().replace('-', ':')
    parts = bssid.split(':')
    if len(parts) < 3:
        return None
    prefix = ':'.join(parts[:3])
    return (oui_map or _default_map()).get(prefix)


__all__ = ["load_oui_map", "lookup_vendor", "update_oui_file"]
