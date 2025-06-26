"""Launch the web UI and open Chromium in kiosk mode."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from piwardrive.cli.kiosk import main

if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
