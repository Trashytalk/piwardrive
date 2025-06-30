#!/usr/bin/env bash
# Pull latest PiWardrive code and restart services.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}/.."
cd "$REPO_ROOT"

echo "Updating repository in $REPO_ROOT"
if ! git pull --ff-only; then
    echo "git pull failed" >&2
    exit 1
fi

services=(service_api piwardrive-webui)

# Use sudo if not running as root
if [ "$(id -u)" -ne 0 ]; then
    SUDO="sudo"
else
    SUDO=""
fi

for svc in "${services[@]}"; do
    if systemctl list-unit-files | grep -q "^${svc}\.service"; then
        echo "Restarting ${svc}.service"
        $SUDO systemctl restart "${svc}.service" || true
    fi
done

