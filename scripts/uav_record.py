"""Record Wi-Fi and GPS data from a UAV using dronekit."""

from __future__ import annotations

import argparse
import logging
import os
import time

from sigint_suite import paths
from sigint_suite.exports import export_json
from sigint_suite.wifi import scan_wifi

from piwardrive.logconfig import setup_logging

try:
    from dronekit import connect
except Exception:  # pragma: no cover - optional dependency
    connect = None


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Record Wi-Fi and GPS data from a drone"
    )
    parser.add_argument(
        "--connect",
        default="127.0.0.1:14550",
        help="vehicle connection string",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="seconds between scans",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=60.0,
        help="recording duration (0 for infinite)",
    )
    parser.add_argument(
        "--export-dir",
        default=paths.EXPORT_DIR,
        help="directory for JSON exports",
    )
    args = parser.parse_args(argv)

    setup_logging(stdout=True)

    if connect is None:
        raise RuntimeError(
            "dronekit not installed. Use 'pip install dronekit' to enable UAV support"
        )

    vehicle = connect(args.connect, wait_ready=True)

    track: list[tuple[float, float]] = []
    wifi_records: list[dict[str, object]] = []
    start = time.time()
    try:
        while True:
            loc = vehicle.location.global_frame
            lat = getattr(loc, "lat", None)
            lon = getattr(loc, "lon", None)
            if lat is not None and lon is not None:
                track.append((float(lat), float(lon)))
                nets = scan_wifi()
                ts = time.time()
                for net in nets:
                    rec = net.model_dump()
                    rec["lat"] = float(lat)
                    rec["lon"] = float(lon)
                    rec["timestamp"] = ts
                    wifi_records.append(rec)
            if args.duration > 0 and time.time() - start >= args.duration:
                break
            time.sleep(args.interval)
    finally:
        vehicle.close()

    os.makedirs(args.export_dir, exist_ok=True)
    export_json(track, os.path.join(args.export_dir, "uav_track.json"))
    export_json(wifi_records, os.path.join(args.export_dir, "uav_wifi.json"))
    logging.info("Data saved to %s", args.export_dir)


if __name__ == "__main__":  # pragma: no cover - manual use
    main()
