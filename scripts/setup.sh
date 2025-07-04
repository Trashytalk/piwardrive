#!/usr/bin/env bash
# Automated setup script for PiWardrive on Debian-based systems
set -euo pipefail

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_ID=${ID}
else
    echo "Unable to detect OS" >&2
    exit 1
fi

case "$OS_ID" in
    ubuntu|debian|raspbian)
        ;;
    *)
        echo "Unsupported platform: $OS_ID" >&2
        exit 1
        ;;
esac

# Use sudo unless running as root
if [ "$(id -u)" -ne 0 ]; then
    SUDO="sudo"
else
    SUDO=""
fi

packages=(git build-essential cmake kismet bettercap gpsd redis-server postgresql python3-venv)

$SUDO apt-get update
$SUDO apt-get install -y "${packages[@]}"

VENV_DIR="${PW_VENV:-pw-env}"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install -r requirements.txt
pip install .

deactivate

cat <<EOM
PiWardrive setup complete.
Activate the environment with:
  source ${VENV_DIR}/bin/activate
Then run the setup wizard:
  python -m piwardrive.setup_wizard
EOM
