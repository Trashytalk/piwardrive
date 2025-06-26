"""Minimal text dashboard for SIGINT scan results.

This module loads JSON exports produced by the helper scripts under
``sigint_suite/scripts`` and prints a concise summary.  It exposes a
``main`` function so it can be executed directly::

    python -m sigint_suite.dashboard

The output defaults to a human readable format but ``--json`` will dump
the raw data instead.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List, Mapping
from .. import paths

DEFAULT_EXPORT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "exports")
)


def _load_json(path: str) -> List[Dict[str, Any]]:
    """Return parsed JSON from ``path`` or an empty list on failure."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []


def load_data(
    export_dir: str = DEFAULT_EXPORT_DIR,
) -> Mapping[str, List[Dict[str, Any]]]:
    """Load Wi-Fi and Bluetooth scan data from ``export_dir``."""
    wifi = _load_json(os.path.join(export_dir, "wifi.json"))
    bluetooth = _load_json(os.path.join(export_dir, "bluetooth.json"))
    return {"wifi": wifi, "bluetooth": bluetooth}


def format_text(data: Mapping[str, List[Dict[str, Any]]]) -> str:
    """Return a compact multi-line summary of the provided ``data``."""
    lines: List[str] = []

    wifi = data.get("wifi", [])
    lines.append(f"Wi-Fi networks: {len(wifi)}")
    for rec in wifi[:5]:
        ssid = rec.get("ssid", "(hidden)")
        bssid = rec.get("bssid", "")
        vendor = rec.get("vendor", "")
        quality = rec.get("quality", "")
        parts = [ssid]
        if bssid:
            parts.append(bssid)
        if vendor:
            parts.append(vendor)
        if quality:
            parts.append(quality)
        lines.append("  " + " ".join(parts))

    lines.append("")

    bt = data.get("bluetooth", [])
    lines.append(f"Bluetooth devices: {len(bt)}")
    for rec in bt[:5]:
        addr = rec.get("address", "")
        name = rec.get("name", "")
        parts = [addr]
        if name:
            parts.append(name)
        lines.append("  " + " ".join(parts))

    return "\n".join(lines)


def main() -> None:  # pragma: no cover - small CLI helper
    """Entry point for ``python -m sigint_suite.dashboard``."""
    parser = argparse.ArgumentParser(description="Show exported scan results")
    parser.add_argument(
        "--export-dir",
        default=paths.EXPORT_DIR,
        help="directory containing JSON exports",
    )
    parser.add_argument("--json", action="store_true", help="print raw JSON")
    args = parser.parse_args()

    data = load_data(args.export_dir)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(format_text(data))


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
