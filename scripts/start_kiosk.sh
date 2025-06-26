#!/usr/bin/env bash
# Start the web UI and API server then open Chromium in kiosk mode.
set -euo pipefail

# Resolve the directory of this script so it works both from source checkouts and
# when installed system wide.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Use the bundled Python helper to launch the server and browser.
exec python3 "$SCRIPT_DIR/kiosk.py" "$@"
