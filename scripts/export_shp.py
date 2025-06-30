import argparse
import asyncio
import logging

from piwardrive.logconfig import setup_logging

try:  # allow tests to substitute a lightweight persistence module
    from persistence import load_ap_cache
except Exception:  # pragma: no cover - fallback
    from piwardrive.persistence import load_ap_cache

from piwardrive import export


def main(argv: list[str] | None = None) -> None:
    """Export saved Wi-Fi access points to a Shapefile."""
    parser = argparse.ArgumentParser(
        description="Export saved access points to a Shapefile"
    )
    parser.add_argument("output", help="destination .shp file")
    parser.add_argument(
        "--fields",
        nargs="+",
        help="subset of fields to include in the output",
    )
    args = parser.parse_args(argv)

    setup_logging(stdout=True)
    records = asyncio.run(load_ap_cache())
    export.export_records(records, args.output, fmt="shp", fields=args.fields)
    logging.info("Saved %s", args.output)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
