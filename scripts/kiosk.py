"""Launch the web UI and open Chromium in kiosk mode."""
from __future__ import annotations

import os
import sys

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

if __name__ == "__main__":  # pragma: no cover - manual invocation
    from piwardrive.cli.kiosk import main  # noqa: E402

    main()
