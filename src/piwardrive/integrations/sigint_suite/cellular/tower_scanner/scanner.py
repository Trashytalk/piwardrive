import asyncio
import logging
import os
import shlex
import subprocess
from typing import List, Optional

from piwardrive.core import config
from piwardrive.scheduler import PollScheduler

from piwardrive.sigint_suite.cellular.parsers import parse_tower_output
from piwardrive.sigint_suite.gps import get_position
from piwardrive.sigint_suite.hooks import apply_post_processors
from piwardrive.sigint_suite.models import TowerRecord

logger = logging.getLogger(__name__)


def _allowed() -> bool:
    cfg = config.AppConfig.load()
    rules = cfg.scan_rules.get("towers", {}) if hasattr(cfg, "scan_rules") else {}
    return PollScheduler.check_rules(rules)


def scan_towers(
    cmd: Optional[str] = None,
    *,
    with_location: bool = True,
    timeout: Optional[int] = None,
) -> List[TowerRecord]:
    """Scan for nearby cell towers and return a list of records."""
    if not _allowed():
        return []
    cmd_str = str(cmd or os.getenv("TOWER_SCAN_CMD", "tower-scan"))
    args = shlex.split(cmd_str)
    timeout = (
        timeout if timeout is not None else int(os.getenv("TOWER_SCAN_TIMEOUT", "10"))
    )
    try:
        output = subprocess.check_output(
            args, text=True, stderr=subprocess.DEVNULL, timeout=timeout
        )
    except Exception as exc:
        logger.exception("Tower scan failed: %s", exc)
        return []

    records = parse_tower_output(output)
    if with_location:
        pos = get_position()
        if pos:
            lat, lon = pos
            for rec in records:
                rec.lat = lat
                rec.lon = lon

    records = apply_post_processors("tower", [r.model_dump() for r in records])
    return [TowerRecord(**rec) for rec in records]


async def async_scan_towers(
    cmd: Optional[str] = None,
    *,
    with_location: bool = True,
    timeout: int | None = None,
) -> List[TowerRecord]:
    """Asynchronously scan for cell towers."""
    if not _allowed():
        return []
    cmd_str = str(cmd or os.getenv("TOWER_SCAN_CMD", "tower-scan"))
    args = shlex.split(cmd_str)
    timeout = (
        timeout if timeout is not None else int(os.getenv("TOWER_SCAN_TIMEOUT", "10"))
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
        logger.exception("Tower scan failed: %s", exc)
        return []

    records = parse_tower_output(output)
    if with_location:
        pos = get_position()
        if pos:
            lat, lon = pos
            for rec in records:
                rec.lat = lat
                rec.lon = lon

    records = apply_post_processors("tower", [r.model_dump() for r in records])
    return [TowerRecord(**rec) for rec in records]
