#!/bin/bash
# Start the web UI and API server then open Chromium in kiosk mode.
set -euo pipefail

piwardrive-kiosk "$@"
