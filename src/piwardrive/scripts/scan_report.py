"""Generate a JSON report summarizing scan results."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging

from piwardrive.logconfig import setup_logging
from piwardrive.scan_report import generate_scan_report


def main(argv: list[str] | None = None) -> None:
    """Print scan summary to stdout."""
    parser = argparse.ArgumentParser(description="Show scan summary")
    parser.add_argument("--json", action="store_true", help="output JSON")
    args = parser.parse_args(argv)

    setup_logging(stdout=True)
    report = asyncio.run(generate_scan_report())
    if args.json:
        print(json.dumps(report))
    else:
        lines = [
            f"Networks: {report['total_networks']}",
            f"Unique SSIDs: {report['unique_ssids']}",
            f"Open networks: {report['open_networks']}",
        ]
        if report["top_ssids"]:
            lines.append("Top SSIDs:")
            for ssid, count in report["top_ssids"]:
                name = ssid or "(hidden)"
                lines.append(f"  {name}: {count}")
        logging.info("\n".join(lines))


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
