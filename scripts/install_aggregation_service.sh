#!/usr/bin/env bash
# Install PiWardrive aggregation server service and dependencies
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$HOME/agg-env"
SERVICE_PATH="/etc/systemd/system/piwardrive-aggregation.service"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is required" >&2
    exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install fastapi aiosqlite 'uvicorn[standard]'
# Install the local package for analysis helpers
pip install "$SCRIPT_DIR/.."

deactivate

cat <<EOF_UNIT | sudo tee "$SERVICE_PATH" >/dev/null
[Unit]
Description=PiWardrive Aggregation Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME
ExecStart=$VENV_DIR/bin/python -m piwardrive.aggregation_service
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF_UNIT

echo "Service written to $SERVICE_PATH"

echo "Enable the service with: sudo systemctl enable --now piwardrive-aggregation.service"

