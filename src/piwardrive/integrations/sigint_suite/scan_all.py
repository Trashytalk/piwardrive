"""Module scan_all."""
import argparse
import os

from piwardrive.sigint_suite.bluetooth import scan_bluetooth
from piwardrive.sigint_suite.cellular.band_scanner import scan_bands
from piwardrive.sigint_suite.cellular.imsi_catcher import scan_imsis
from piwardrive.sigint_suite.cellular.tower_scanner import scan_towers
from piwardrive.sigint_suite.exports import export_json
from piwardrive.sigint_suite.wifi import scan_wifi

DEFAULT_EXPORT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "exports"))


def run_once(export_dir: str) -> None:
    os.makedirs(export_dir, exist_ok=True)
    wifi_data = scan_wifi()
    bt_data = scan_bluetooth()
    band_data = scan_bands()
    imsi_data = scan_imsis()
    tower_data = scan_towers()
    export_json(wifi_data, os.path.join(export_dir, "wifi.json"))
    export_json(bt_data, os.path.join(export_dir, "bluetooth.json"))
    export_json(band_data, os.path.join(export_dir, "bands.json"))
    export_json(imsi_data, os.path.join(export_dir, "imsis.json"))
    export_json(tower_data, os.path.join(export_dir, "towers.json"))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Run all wireless scans and export to JSON"
    )
    parser.add_argument(
        "--export-dir",
        default=os.environ.get("EXPORT_DIR", DEFAULT_EXPORT_DIR),
        help="directory to store JSON results",
    )
    args = parser.parse_args(argv)
    run_once(args.export_dir)


if __name__ == "__main__":  # pragma: no cover - manual use
    main()
