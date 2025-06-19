#!/bin/bash
# Start the web UI and API server then open Chromium in kiosk mode.
set -euo pipefail

URL="http://localhost:8000"

piwardrive-webui &
PID=$!

# Give the server a moment to start
sleep 2

# Prefer chromium-browser but fall back to chromium
if command -v chromium-browser >/dev/null 2>&1; then
    BROWSER=chromium-browser
else
    BROWSER=chromium
fi

"$BROWSER" --kiosk "$URL"

# Stop the API when the browser exits
kill "$PID"
