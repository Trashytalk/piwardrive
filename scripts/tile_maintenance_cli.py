"""Lightweight command line interface for tile cache maintenance."""
import argparse
from types import SimpleNamespace


def purge_old_tiles(folder: str, days: int) -> None:
    """Lazy wrapper around :func:`tile_maintenance.purge_old_tiles`."""
    from piwardrive.map import tile_maintenance as tm  # heavy import deferred
    tm.purge_old_tiles(folder, days)


def enforce_cache_limit(folder: str, limit: int) -> None:
    """Lazy wrapper around :func:`tile_maintenance.enforce_cache_limit`."""
    from piwardrive.map import tile_maintenance as tm
    tm.enforce_cache_limit(folder, limit)


def vacuum_mbtiles(path: str) -> None:
    """Lazy wrapper around :func:`tile_maintenance.vacuum_mbtiles`."""
    from piwardrive.map import tile_maintenance as tm
    tm.vacuum_mbtiles(path)


# Object used by tests to monkey patch the maintenance functions without forcing
# the optional heavy imports above.  The wrappers import the real implementations
# only when executed.
tile_maintenance = SimpleNamespace(
    purge_old_tiles=purge_old_tiles,
    enforce_cache_limit=enforce_cache_limit,
    vacuum_mbtiles=vacuum_mbtiles,
)


def main(argv: list[str] | None = None) -> None:
    """Run tile cache maintenance tasks."""
    parser = argparse.ArgumentParser(description="Maintain offline map tiles")
    parser.add_argument(
        "--folder",
        default="/mnt/ssd/tiles",
        help="tile cache directory",
    )
    parser.add_argument(
        "--offline",
        help="path to offline MBTiles file",
    )
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=30,
        help="age in days for --purge",
    )
    parser.add_argument(
        "--limit-mb",
        type=int,
        default=512,
        help="cache size limit for --limit",
    )
    parser.add_argument("--purge", action="store_true", help="delete old tiles")
    parser.add_argument(
        "--limit",
        action="store_true",
        dest="limit_op",
        help="enforce cache size limit",
    )
    parser.add_argument(
        "--vacuum",
        action="store_true",
        help="VACUUM the offline MBTiles file",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="run all maintenance operations",
    )
    args = parser.parse_args(argv)

    run_purge = args.all or args.purge
    run_limit = args.all or args.limit_op
    run_vacuum = args.all or args.vacuum

    if run_purge:
        tile_maintenance.purge_old_tiles(args.folder, args.max_age_days)
    if run_limit:
        tile_maintenance.enforce_cache_limit(args.folder, args.limit_mb)
    if args.offline and run_vacuum:
        tile_maintenance.vacuum_mbtiles(args.offline)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
