"""Module prefetch_cli."""
import argparse
from piwardrive.screens.map_utils import tile_cache


def main(argv: list[str] | None = None) -> None:
    """Prefetch map tiles for the given bounding box."""
    parser = argparse.ArgumentParser(description="Download map tiles to cache")
    parser.add_argument("min_lat", type=float, help="minimum latitude")
    parser.add_argument("min_lon", type=float, help="minimum longitude")
    parser.add_argument("max_lat", type=float, help="maximum latitude")
    parser.add_argument("max_lon", type=float, help="maximum longitude")
    parser.add_argument("--zoom", type=int, default=16, help="tile zoom level")
    parser.add_argument(
        "--folder",
        default="/mnt/ssd/tiles",
        help="destination folder for downloaded tiles",
    )
    parser.add_argument("--concurrency", type=int, help="number of concurrent requests")
    args = parser.parse_args(argv)

    def progress(done: int, total: int) -> None:
        print(f"{done}/{total}", end="\r", flush=True)

    tile_cache.prefetch_tiles(
        (args.min_lat, args.min_lon, args.max_lat, args.max_lon),
        zoom=args.zoom,
        folder=args.folder,
        concurrency=args.concurrency,
        progress_cb=progress,
    )


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
