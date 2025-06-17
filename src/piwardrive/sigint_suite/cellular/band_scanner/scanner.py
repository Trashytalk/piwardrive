"""Module scanner."""
import logging
import os
import shlex
import subprocess
import asyncio
from typing import List, Optional


from sigint_suite.cellular.parsers import parse_band_output
from sigint_suite.models import BandRecord

logger = logging.getLogger(__name__)


def scan_bands(
    cmd: Optional[str] = None,
    timeout: int | None = None,
) -> List[BandRecord]:

    """Scan for cellular bands and return a list of records.

    The command output is expected to be comma separated with
    ``band,channel,rssi`` per line. Set the ``BAND_SCAN_CMD`` environment
    variable to override the executable. The timeout defaults to the
    ``BAND_SCAN_TIMEOUT`` environment variable (``10`` seconds).
    """

    cmd_str = cmd or os.getenv("BAND_SCAN_CMD", "celltrack")
    args = shlex.split(cmd_str)
    timeout = (
        timeout if timeout is not None else int(os.getenv("BAND_SCAN_TIMEOUT", "10"))
    )
    try:
        output = subprocess.check_output(
            args, text=True, stderr=subprocess.DEVNULL, timeout=timeout
        )
    except Exception as exc:
        logger.exception("Band scan failed: %s", exc)

        return []

    return parse_band_output(output)


async def async_scan_bands(
    cmd: Optional[str] = None,
    timeout: int | None = None,
) -> List[BandRecord]:
    """Asynchronously scan for cellular bands using ``celltrack``."""

    cmd_str = cmd or os.getenv("BAND_SCAN_CMD", "celltrack")
    args = shlex.split(cmd_str)
    timeout = (
        timeout if timeout is not None else int(os.getenv("BAND_SCAN_TIMEOUT", "10"))
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
    except Exception as exc:  # pragma: no cover - external command
        logger.exception("Band scan failed: %s", exc)
        return []

    return parse_band_output(output)


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Scan cellular bands")
    parser.add_argument("--cmd", default=None, help="band scan command")
    parser.add_argument("--json", action="store_true", help="print results as JSON")
    args = parser.parse_args()

    data = scan_bands(args.cmd)
    if args.json:
        print(json.dumps([r.model_dump() for r in data], indent=2))
    else:
        for rec in data:
            print(f"{rec.band} {rec.channel} {rec.rssi}")


if __name__ == "__main__":
    main()
