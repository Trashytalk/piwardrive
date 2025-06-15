#!/bin/bash
# Install system and Python dependencies required for scanning utilities.
#
# Required tools:
#   - sudo privileges with apt-get
#   - python3 and pip
#
# Missing Python packages from requirements.txt will be installed if not present.
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

sudo apt-get update
sudo apt-get install -y wireless-tools bluez
python3 -m pip install --upgrade pip

missing_pkg=0
while IFS= read -r line; do
    pkg=$(echo "$line" | sed 's/[>=<].*//' | xargs)
    [[ -z "$pkg" || $pkg == \#* ]] && continue
    if ! python3 -m pip show "$pkg" >/dev/null 2>&1; then
        missing_pkg=1
        break
    fi
done < "$ROOT_DIR/requirements.txt"

if [ $missing_pkg -eq 1 ]; then
    python3 -m pip install -r "$ROOT_DIR/requirements.txt"
fi

$SCRIPT_DIR/fetch_oui.sh

echo "Setup complete"
