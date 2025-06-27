"""Interactive orientation calibration helper."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Dict

from piwardrive import orientation_sensors as osens
from piwardrive.logconfig import setup_logging


def _prompt(angle: float) -> None:
    input(f"Rotate the device to {angle} degrees and press Enter...")
    orient = osens.get_orientation_dbus()
    if orient is None:
        logging.error("Orientation not available, skipping")
        return
    osens.update_orientation_map({orient: angle})
    logging.info("Mapped '%s' -> %s", orient, angle)


def main(argv: list[str] | None = None) -> None:
    """Guide the user through orientation calibration."""
    parser = argparse.ArgumentParser(
        description="Record orientation angles from the device sensors",
    )
    parser.add_argument(
        "--output",
        default="orientation_map.json",
        help="Destination JSON file",
    )
    args = parser.parse_args(argv)

    setup_logging(stdout=True)

    mapping: Dict[str, float] = {}
    for angle in (0.0, 90.0, 180.0, 270.0):
        _prompt(angle)
    mapping = osens.clone_orientation_map()
    Path(args.output).write_text(json.dumps(mapping, indent=2))
    logging.info("Saved mapping to %s", args.output)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
