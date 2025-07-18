#!/bin/bash
# Quick environment setup for PiWardrive on Debian-based systems
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Required system packages
packages=(git build-essential cmake kismet bettercap gpsd evtest python3-venv curl libsqlcipher-dev)

# Check for apt-get
if ! command -v apt-get >/dev/null 2>&1; then
    echo "apt-get not found. Install required packages manually." >&2
    exit 1
fi

# Check for Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is required." >&2
    exit 1
fi

if ! python3 -m venv --help >/dev/null 2>&1; then
    echo "python3-venv is not installed." >&2
    exit 1
fi

# Use sudo unless running as root
if [ "$(id -u)" -ne 0 ]; then
    SUDO="sudo"
else
    SUDO=""
fi

$SUDO apt-get update
$SUDO apt-get install -y "${packages[@]}"

VENV_DIR="gui-env"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install -r requirements.txt
pip install pysqlcipher3
pip install .

echo "Fetching latest OUI registry..."
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
bash "$ROOT_DIR/src/piwardrive/integrations/sigint_suite/scripts/fetch_oui.sh"

if [ -n "${PW_DB_KEY:-}" ]; then
    echo "Initializing encrypted database..."
    piwardrive-migrate
fi

cat <<EOM
Setup complete. Activate the environment with:
  source ${VENV_DIR}/bin/activate
EOM

