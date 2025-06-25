"""Interactive orientation calibration helper."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict

from piwardrive import orientation_sensors as osens


def _prompt(angle: float) -> None:
    input(f"Rotate the device to {angle} degrees and press Enter...")
    orient = osens.get_orientation_dbus()
    if orient is None:
        print("Orientation not available, skipping")
        return
    osens.update_orientation_map({orient: angle})
    print(f"Mapped '{orient}' -> {angle}")


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

    mapping: Dict[str, float] = {}
    for angle in (0.0, 90.0, 180.0, 270.0):
        _prompt(angle)
    mapping = osens.clone_orientation_map()
    Path(args.output).write_text(json.dumps(mapping, indent=2))
    print(f"Saved mapping to {args.output}")


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
