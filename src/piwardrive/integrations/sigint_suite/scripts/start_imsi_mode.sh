#!/bin/bash
# Collect Wi-Fi and Bluetooth data and export to JSON files.
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
# Allow callers to override the output directory via EXPORT_DIR
EXPORT_DIR="${EXPORT_DIR:-$ROOT_DIR/exports}"

mkdir -p "$EXPORT_DIR"

PYTHONPATH="$ROOT_DIR/.." EXPORT_DIR="$EXPORT_DIR" python3 - <<'PY'
import os
from piwardrive.sigint_suite.wifi import scan_wifi
from piwardrive.sigint_suite.bluetooth import scan_bluetooth
from piwardrive.sigint_suite.exports import export_json

export_dir = os.environ["EXPORT_DIR"]
export_json(scan_wifi(), os.path.join(export_dir, "wifi.json"))
export_json(scan_bluetooth(), os.path.join(export_dir, "bluetooth.json"))
PY

echo "Data saved to $EXPORT_DIR"

