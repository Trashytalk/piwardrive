#!/usr/bin/env python3
"""Validate a PiWardrive configuration file."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from piwardrive import config


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Validate a configuration file")
    parser.add_argument(
        "path",
        nargs="?",
        default=config.get_config_path(),
        help="Path to config file",
    )
    args = parser.parse_args(argv)

    try:
        data = json.loads(Path(args.path).read_text())
        config.validate_config_data(data)
    except Exception as exc:
        logging.error("Invalid configuration: %s", exc)
        raise SystemExit(1)
    print("Configuration OK")


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
