#!/bin/bash
# Install system and Python dependencies required for scanning utilities.
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

sudo apt-get update
sudo apt-get install -y wireless-tools bluez
python3 -m pip install --upgrade pip
python3 -m pip install -r "$ROOT_DIR/requirements.txt"

echo "Setup complete"
