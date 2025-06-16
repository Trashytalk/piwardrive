import argparse
import os
import time

from sigint_suite.bluetooth import scan_bluetooth
from sigint_suite.exports import export_json
from sigint_suite.wifi import scan_wifi

DEFAULT_EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "exports")


def run_once(export_dir: str) -> None:
    wifi_data = scan_wifi()
    bt_data = scan_bluetooth()
    export_json(wifi_data, os.path.join(export_dir, "wifi.json"))
    export_json(bt_data, os.path.join(export_dir, "bluetooth.json"))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Continuously scan wireless data")
    parser.add_argument(
        "--interval",
        "-i",
        type=float,
        default=60.0,
        help="Seconds between scans",
    )
    parser.add_argument(
        "--iterations",
        "-n",
        type=int,
        default=0,
        help="Number of scans to run (0 for infinite)",
    )
    parser.add_argument(
        "--export-dir",
        default=os.environ.get("EXPORT_DIR", DEFAULT_EXPORT_DIR),
        help="Directory to store JSON results",
    )
    args = parser.parse_args(argv)

    os.makedirs(args.export_dir, exist_ok=True)

    count = 0
    while True:
        run_once(args.export_dir)
        count += 1
        if args.iterations and count >= args.iterations:
            break
        time.sleep(args.interval)


if __name__ == "__main__":  # pragma: no cover - manual use
    main()
