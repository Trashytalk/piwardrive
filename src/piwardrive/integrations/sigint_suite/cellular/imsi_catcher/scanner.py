"""Module scanner."""

import asyncio
import logging
import subprocess
from typing import Any, Callable, List, Optional, cast

from piwardrive.core import config
from piwardrive.scheduler import PollScheduler
from piwardrive.sigint_suite.cellular.parsers import parse_imsi_output
from piwardrive.sigint_suite.gps import get_position
from piwardrive.sigint_suite.hooks import apply_post_processors
from piwardrive.sigint_suite.models import ImsiRecord

from ..utils import build_cmd_args

logger = logging.getLogger(__name__)


def _allowed() -> bool:
    cfg = config.AppConfig.load()
    rules = cfg.scan_rules.get("imsi", {}) if hasattr(cfg, "scan_rules") else {}
    return PollScheduler.check_rules(rules)


def scan_imsis(
    cmd: Optional[str] = None,
    with_location: bool = True,
    enrich_func: Optional[Callable[[List[ImsiRecord]], List[ImsiRecord]]] = None,
    timeout: Optional[int] = None,
) -> List[dict[str, Any]]:
    """Scan for IMSI numbers using an external command."""
    if not _allowed():
        return []
    args, timeout = build_cmd_args(
        cmd,
        "IMSI_CATCH_CMD",
        "imsi-catcher",
        timeout,
        "IMSI_SCAN_TIMEOUT",
    )
    try:
        output = subprocess.check_output(
            args, text=True, stderr=subprocess.DEVNULL, timeout=timeout
        )
    except Exception as exc:  # pragma: no cover - external command
        logging.exception("Failed to run IMSI catcher", exc_info=exc)
        return []

    records = cast(List[ImsiRecord], parse_imsi_output(output))

    if with_location:
        pos = get_position()
        if pos:
            lat, lon = pos
            for rec in records:
                rec.lat = lat
                rec.lon = lon

    records = apply_post_processors("imsi", records)

    if enrich_func:
        try:
            records = list(enrich_func(records))
        except Exception:
            pass

    return [r.model_dump() for r in records]


async def async_scan_imsis(
    cmd: Optional[str] = None,
    with_location: bool = True,
    enrich_func: Optional[Callable[[List[ImsiRecord]], List[ImsiRecord]]] = None,
    timeout: int | None = None,
) -> List[ImsiRecord]:
    """Asynchronously scan for IMSI numbers."""
    if not _allowed():
        return []
    args, timeout = build_cmd_args(
        cmd,
        "IMSI_CATCH_CMD",
        "imsi-catcher",
        timeout,
        "IMSI_SCAN_TIMEOUT",
    )
    logger.debug("Executing: %s", " ".join(args))
    try:
        proc = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        output = stdout.decode()
    except Exception as exc:
        logger.exception("IMSI scan failed: %s", exc)
        return []

    records = cast(List[ImsiRecord], parse_imsi_output(output))

    if with_location:
        pos = get_position()
        if pos:
            lat, lon = pos
            for rec in records:
                rec.lat = lat
                rec.lon = lon

    records = apply_post_processors("imsi", records)

    if enrich_func:
        try:
            records = list(enrich_func(records))
        except Exception:
            pass

    return records


def main() -> None:  # pragma: no cover - CLI helper
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Scan for IMSI numbers")
    parser.add_argument("--cmd", default=None, help="IMSI catcher command")
    parser.add_argument("--json", action="store_true", help="print results as JSON")
    parser.add_argument(
        "--no-location", action="store_true", help="disable GPS tagging"
    )
    args = parser.parse_args()

    data = scan_imsis(args.cmd, with_location=not args.no_location)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        for rec in data:
            fields = [
                rec.get("imsi", ""),
                rec.get("mcc", ""),
                rec.get("mnc", ""),
                rec.get("rssi", ""),
            ]
            if rec.get("lat") is not None and rec.get("lon") is not None:
                fields.extend(
                    [
                        str(rec.get("lat")),
                        str(rec.get("lon")),
                    ]
                )
            print(" ".join(fields))


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
