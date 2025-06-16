import os
import shlex
import subprocess
from typing import List, Optional, Callable

from sigint_suite.models import ImsiRecord

from sigint_suite.cellular.parsers import parse_imsi_output
from sigint_suite.gps import get_position
from sigint_suite.hooks import apply_post_processors


def scan_imsis(
    cmd: Optional[str] = None,
    with_location: bool = True,
    enrich_func: Optional[
        Callable[[List[ImsiRecord]], List[ImsiRecord]]
    ] = None,
    timeout: int | None = None,
) -> List[ImsiRecord]:

    """Scan for IMSI numbers using an external command.

    The command output should be comma separated with ``imsi,mcc,mnc,rssi`` per
    line. Set the ``IMSI_CATCH_CMD`` environment variable to override the
    executable. If ``with_location`` is True, each record will be tagged with the
    current GPS position when available. ``enrich_func`` can be used to
    post-process the records (e.g., look up operators).
    """

    cmd_str = cmd or os.getenv("IMSI_CATCH_CMD", "imsi-catcher")
    args = shlex.split(cmd_str)
    timeout = timeout if timeout is not None else int(os.getenv("IMSI_SCAN_TIMEOUT", "10"))
    try:
        output = subprocess.check_output(
            args, text=True, stderr=subprocess.DEVNULL, timeout=timeout
        )
    except Exception:
        return []

    records = parse_imsi_output(output)

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


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Scan for IMSI numbers")
    parser.add_argument("--cmd", default=None, help="IMSI catcher command")
    parser.add_argument("--json", action="store_true", help="print results as JSON")
    parser.add_argument(
        "--no-location",
        action="store_true",
        help="disable GPS tagging",
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
            if "lat" in rec and "lon" in rec:
                fields.extend([str(rec["lat"]), str(rec["lon"])])
            print(" ".join(fields))


if __name__ == "__main__":
    main()
