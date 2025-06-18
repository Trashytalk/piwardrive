#!/bin/bash
# Install the PiWardrive aggregation service.
# Sets up a Python virtual environment and writes a systemd unit.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="agg-env"

# Required system packages
packages=(python3-venv)

if command -v apt-get >/dev/null 2>&1; then
    if [ "$(id -u)" -ne 0 ]; then
        SUDO="sudo"
    else
        SUDO=""
    fi
    $SUDO apt-get update
    $SUDO apt-get install -y "${packages[@]}"
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is required." >&2
    exit 1
fi

if ! python3 -m venv --help >/dev/null 2>&1; then
    echo "python3-venv is required." >&2
    exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install fastapi uvicorn aiosqlite
pip install "$ROOT_DIR"

echo "Writing systemd service..."
UNIT_PATH="/etc/systemd/system/piwardrive-aggregation.service"
SERVICE_CMD="$ROOT_DIR/$VENV_DIR/bin/python -m piwardrive.aggregation_service"

if [ "$(id -u)" -ne 0 ]; then
    SUDO="sudo"
else
    SUDO=""
fi

$SUDO tee "$UNIT_PATH" >/dev/null <<EOM
[Unit]
Description=PiWardrive Aggregation Service
After=network.target

[Service]
Type=simple
WorkingDirectory=$ROOT_DIR
ExecStart=$SERVICE_CMD
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOM

echo "Service installed to $UNIT_PATH"
echo "Enable with: sudo systemctl enable --now piwardrive-aggregation.service"
