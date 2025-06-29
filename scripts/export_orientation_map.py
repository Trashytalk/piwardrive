import argparse
import json
import logging
from pathlib import Path

from piwardrive import orientation_sensors as osens
from piwardrive.logconfig import setup_logging


def main(argv: list[str] | None = None) -> None:
    """Write the current orientation map to JSON."""
    parser = argparse.ArgumentParser(
        description="Export the orientation map to a JSON file",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="orientation_map.json",
        help="destination JSON file",
    )
    args = parser.parse_args(argv)

    setup_logging(stdout=True)
    mapping = osens.clone_orientation_map()
    Path(args.output).write_text(json.dumps(mapping, indent=2))
    logging.info("Saved mapping to %s", args.output)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
