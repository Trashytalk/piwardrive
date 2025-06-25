"""Module tile_maintenance_cli."""
import argparse
from piwardrive import tile_maintenance


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
