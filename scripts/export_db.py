"""Export Wi-Fi data from the PiWardrive database."""

import argparse
import asyncio
import logging

from piwardrive.logconfig import setup_logging
from pwutils import database

EXPORT_FORMATS = ("csv", "json", "gpx", "kml")


def main(argv: list[str] | None = None) -> None:
    """Export access point cache to a file."""
    parser = argparse.ArgumentParser(description="Export database records")
    parser.add_argument("output", help="destination file")
    parser.add_argument(
        "--format",
        "-f",
        choices=EXPORT_FORMATS,
        default="csv",
        help="output format",
    )
    parser.add_argument("--fields", nargs="+", help="subset of fields to include")
    args = parser.parse_args(argv)

    setup_logging(stdout=True)
    asyncio.run(database.export_ap_cache(args.output, args.format, args.fields))
    logging.info("Saved %s", args.output)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
