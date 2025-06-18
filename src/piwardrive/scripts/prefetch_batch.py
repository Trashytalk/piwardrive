"""Module prefetch_batch."""
import argparse
from screens.map_utils import tile_cache


def _parse_bboxes(path: str) -> list[tuple[float, float, float, float]]:
    bboxes = []
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "," in line:
                parts = line.split(",")
            else:
                parts = line.split()
            if len(parts) < 4:
                print(f"Skipping line {lineno}: {line}")
                continue
            try:
                box = tuple(map(float, parts[:4]))
            except ValueError:
                print(f"Skipping line {lineno}: {line}")
                continue
            bboxes.append(box)  # type: ignore[arg-type]
    return bboxes


def main(argv: list[str] | None = None) -> None:
    """Prefetch tiles for bounding boxes listed in a file."""
    parser = argparse.ArgumentParser(description="Download tiles for multiple bounding boxes")
    parser.add_argument("input", help="path to file with bounding boxes")
    parser.add_argument("--zoom", type=int, default=16, help="tile zoom level")
    parser.add_argument("--folder", default="/mnt/ssd/tiles", help="destination folder")
    parser.add_argument("--concurrency", type=int, help="number of concurrent requests")
    args = parser.parse_args(argv)

    bboxes = _parse_bboxes(args.input)
    if not bboxes:
        print("No bounding boxes found")
        return

    def progress(done: int, total: int) -> None:
        print(f"{done}/{total}", end="\r", flush=True)

    for bbox in bboxes:
        tile_cache.prefetch_tiles(
            bbox,
            zoom=args.zoom,
            folder=args.folder,
            concurrency=args.concurrency,
            progress_cb=progress,
        )


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
