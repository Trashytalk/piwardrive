#!/bin/bash
# Download the IEEE OUI registry for vendor lookups.
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.config/piwardrive"
URL="https://standards-oui.ieee.org/oui/oui.csv"

mkdir -p "$DATA_DIR"
curl -L "$URL" -o "$DATA_DIR/oui.csv"
echo "OUI data saved to $DATA_DIR/oui.csv"
