import asyncio
import json
import os
from collections import Counter
from datetime import datetime
from typing import Any, Dict, Iterable

from . import config
from .persistence import load_ap_cache


def _sync_load(
    records: Iterable[dict[str, Any]] | Iterable[Any],
) -> list[dict[str, Any]]:
    return list(records)


async def _load_records() -> list[dict[str, Any]]:
    records = load_ap_cache()
    if asyncio.iscoroutine(records):
        records = await records
    return _sync_load(records)


async def generate_scan_report() -> Dict[str, Any]:
    data = await _load_records()
    total = len(data)
    ssids = Counter((r.get("ssid") or "") for r in data)
    open_count = sum(1 for r in data if not r.get("encryption"))
    top_ssids = ssids.most_common(5)
    return {
        "timestamp": datetime.now().isoformat(),
        "total_networks": total,
        "unique_ssids": len(ssids),
        "open_networks": open_count,
        "top_ssids": top_ssids,
    }


async def write_scan_report(path: str | None = None) -> str:
    cfg = config.AppConfig.load()
    os.makedirs(cfg.reports_dir, exist_ok=True)
    report = await generate_scan_report()
    if path is None:
        date = datetime.now().strftime("%Y%m%d")
        path = os.path.join(cfg.reports_dir, f"scans_{date}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    return path


__all__ = ["generate_scan_report", "write_scan_report"]
