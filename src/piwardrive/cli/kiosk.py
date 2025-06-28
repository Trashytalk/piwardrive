"""Command line utility to start PiWardrive in browser kiosk mode."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import time
from typing import Sequence

DEFAULT_URL = "http://localhost:8000"


def main(argv: Sequence[str] | None = None) -> None:
    """Launch the dashboard using Chromium in kiosk mode."""
    parser = argparse.ArgumentParser(
        description="Start the API server and open Chromium in kiosk mode"
    )
    parser.add_argument("--url", default=DEFAULT_URL, help="dashboard URL to open")
    parser.add_argument(
        "--delay", type=float, default=2.0, help="seconds to wait for the server"
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    proc = subprocess.Popen(["piwardrive-webui"])
    try:
        time.sleep(args.delay)
        browser = shutil.which("chromium-browser") or shutil.which("chromium")
        if browser is None:
            raise FileNotFoundError("Chromium browser not found")
        subprocess.run([browser, "--kiosk", args.url], check=True)
    finally:
        proc.terminate()


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
