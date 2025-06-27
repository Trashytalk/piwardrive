"""Module export_log_bundle."""
import argparse
import asyncio
import logging

from piwardrive.logconfig import setup_logging
try:  # allow tests to substitute a lightweight main module
    from main import PiWardriveApp  # type: ignore
except Exception:  # pragma: no cover - fallback
    from piwardrive.main import PiWardriveApp


def main(argv: list[str] | None = None) -> None:
    """Bundle recent log files into an archive."""
    parser = argparse.ArgumentParser(description="Export a bundled archive of logs")
    parser.add_argument("output", nargs="?", help="Output file path")
    parser.add_argument(
        "--lines",
        "-n",
        type=int,
        default=200,
        help="Number of lines from each log to include",
    )
    args = parser.parse_args(argv)

    setup_logging(stdout=True)
    app = PiWardriveApp()
    path = asyncio.run(app.export_log_bundle(args.output, args.lines))
    if path:
        logging.info("%s", path)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
