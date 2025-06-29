#!/usr/bin/env bash
# Launch containers/services needed for integration tests.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}/.."

cd "$REPO_ROOT"

if ! command -v docker >/dev/null 2>&1; then
    echo "docker is required" >&2
    exit 1
fi

# Use docker compose (plugin or standalone)
if command -v docker-compose >/dev/null 2>&1; then
    compose() { docker-compose "$@"; }
else
    compose() { docker compose "$@"; }
fi

echo "Starting integration test environment..."
compose up -d

echo "Services are running. Stop them with 'docker compose down'."
