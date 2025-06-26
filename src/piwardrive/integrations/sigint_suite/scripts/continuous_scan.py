"""Module continuous_scan."""
import argparse
import os

from piwardrive.sigint_suite import paths
from piwardrive.sigint_suite.exports import export_json
from piwardrive.sigint_suite import continuous_scan


def _save_results(export_dir: str, results: continuous_scan.Result) -> None:
    export_json(results["wifi"], os.path.join(export_dir, "wifi.json"))
    export_json(results["bluetooth"], os.path.join(export_dir, "bluetooth.json"))


def run_once(export_dir: str) -> None:
    """Perform one scan cycle and write JSON files."""
    _save_results(export_dir, continuous_scan.scan_once())


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
        default=paths.EXPORT_DIR,
        help="Directory to store JSON results",
    )
    args = parser.parse_args(argv)

    os.makedirs(args.export_dir, exist_ok=True)

    continuous_scan.run_continuous_scan(
        interval=args.interval,
        iterations=args.iterations,
        on_result=lambda res: _save_results(args.export_dir, res),
    )


if __name__ == "__main__":  # pragma: no cover - manual use
    main()
