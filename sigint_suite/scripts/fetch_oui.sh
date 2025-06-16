#!/bin/bash
# Download the IEEE OUI registry for vendor lookups.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$(python3 -c 'from sigint_suite import paths; print(paths.CONFIG_DIR)')"
URL="https://standards-oui.ieee.org/oui/oui.csv"

mkdir -p "$DATA_DIR"

MAX_RETRIES=3
RETRY_DELAY=5
attempt=1
while true; do
    if curl -L "$URL" -o "$DATA_DIR/oui.csv"; then
        echo "OUI data saved to $DATA_DIR/oui.csv"
        break
    elif [ $attempt -lt $MAX_RETRIES ]; then
        echo "Download failed (attempt $attempt/$MAX_RETRIES). Retrying in $RETRY_DELAY seconds..." >&2
        attempt=$((attempt+1))
        sleep $RETRY_DELAY
    else
        echo "Failed to download OUI data after $MAX_RETRIES attempts." >&2
        exit 1
    fi
done
