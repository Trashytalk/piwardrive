"""Replay UAV GPS tracks using :func:`gps_track_playback.playback_track`."""

from __future__ import annotations

import argparse
import asyncio
import json

from piwardrive.gps_track_playback import playback_track


async def _print_point(lat: float, lon: float) -> None:
    print(f"{lat:.6f}, {lon:.6f}")


async def _run(track_file: str, interval: float) -> None:
    with open(track_file, "r", encoding="utf-8") as fh:
        points = json.load(fh)
    await playback_track(points, _print_point, interval=interval)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Replay a UAV GPS track")
    parser.add_argument("track", help="JSON track file from uav-record")
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="seconds between points",
    )
    args = parser.parse_args(argv)
    asyncio.run(_run(args.track, args.interval))


if __name__ == "__main__":  # pragma: no cover - manual use
    main()
