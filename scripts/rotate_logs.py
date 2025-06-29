"""Rotate log files listed in the default configuration."""

from __future__ import annotations

import argparse
import logging

from piwardrive import config, diagnostics
from piwardrive.logconfig import setup_logging


def main(argv: list[str] | None = None) -> None:
    """Rotate configured log files."""
    parser = argparse.ArgumentParser(description="Rotate log files")
    parser.add_argument(
        "paths",
        nargs="*",
        help="files to rotate (defaults to config.DEFAULT_CONFIG.log_paths)",
    )
    parser.add_argument(
        "--max-files",
        "-n",
        type=int,
        default=config.DEFAULT_CONFIG.log_rotate_archives,
        help="number of archives to keep",
    )
    args = parser.parse_args(argv)

    setup_logging(stdout=True)

    log_paths = args.paths or list(config.DEFAULT_CONFIG.log_paths)
    for path in log_paths:
        try:
            diagnostics.rotate_log(path, max_files=args.max_files)
            logging.info("Rotated %s", path)
        except Exception:
            logging.exception("Failed to rotate %s", path)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
