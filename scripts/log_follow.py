"""Module log_follow."""

import argparse
import logging
import os
import time

from logconfig import DEFAULT_LOG_PATH
from utils import tail_file

from piwardrive.logconfig import setup_logging


def main(argv: list[str] | None = None) -> None:
    """Continuously print new lines from a log file."""
    parser = argparse.ArgumentParser(description="Follow a log file")
    parser.add_argument(
        "path",
        nargs="?",
        default=DEFAULT_LOG_PATH,
        help="log file path",
    )
    parser.add_argument(
        "--lines",
        "-n",
        type=int,
        default=10,
        help="number of initial lines to show",
    )
    parser.add_argument(
        "--interval",
        "-i",
        type=float,
        default=1.0,
        help="seconds between checks for new data",
    )
    args = parser.parse_args(argv)

    setup_logging(stdout=True)

    for line in tail_file(args.path, args.lines):
        logging.info(line)

    try:
        with open(args.path, "r", encoding="utf-8", errors="ignore") as fh:
            fh.seek(0, os.SEEK_END)
            while True:
                line = fh.readline()
                if line:
                    logging.info(line.rstrip())
                else:
                    time.sleep(args.interval)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
