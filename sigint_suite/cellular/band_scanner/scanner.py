import logging
import os
import shlex
import subprocess
from typing import List, Optional

from sigint_suite.models import BandRecord
from sigint_suite.cellular.parsers import parse_band_output


def scan_bands(cmd: Optional[str] = None, timeout: int | None = None) -> List[BandRecord]:
    """Scan for cellular bands and return a list of records."""

    cmd_str = cmd or os.getenv("BAND_SCAN_CMD", "celltrack")
    args = shlex.split(cmd_str)
    timeout = (
        timeout
        if timeout is not None
        else int(os.getenv("BAND_SCAN_TIMEOUT", "10"))
    )
    try:
        output = subprocess.check_output(
            args, text=True, stderr=subprocess.DEVNULL, timeout=timeout
        )
    except Exception as exc:  # pragma: no cover - external command
        logging.exception("Failed to run band scanner", exc_info=exc)
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
