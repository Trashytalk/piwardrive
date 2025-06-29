"""Delete tile cache entries older than a specified age."""

import argparse

from piwardrive.map import tile_maintenance as tm


def main(argv: list[str] | None = None) -> None:
    """Remove tiles older than ``--max-age-days``."""
    parser = argparse.ArgumentParser(description="Prune old map tiles")
    parser.add_argument(
        "--folder", default="/mnt/ssd/tiles", help="tile cache directory"
    )
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=30,
        help="delete tiles older than this many days",
    )
    args = parser.parse_args(argv)

    tm.purge_old_tiles(args.folder, args.max_age_days)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
