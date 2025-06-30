#!/usr/bin/env bash
# Generate gettext POT template for PiWardrive
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}/.."
POT_DIR="${REPO_ROOT}/locales"

cd "$REPO_ROOT"
mkdir -p "$POT_DIR"

xgettext --from-code=UTF-8 --language=Python --keyword=_ \
    -o "$POT_DIR/piwardrive.pot" \
    $(git ls-files '*.py')

echo "POT file written to $POT_DIR/piwardrive.pot"
