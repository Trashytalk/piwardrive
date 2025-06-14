#!/bin/bash
# Run a single passive scan and export results.
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$SCRIPT_DIR/start_imsi_mode.sh"

