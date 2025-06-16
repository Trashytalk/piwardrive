#!/bin/bash
# Convert captured JSON data into CSV format.
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
EXPORT_DIR="${EXPORT_DIR:-$(python3 -c 'from sigint_suite import paths; print(paths.EXPORT_DIR)') }"

PYTHONPATH="$ROOT_DIR/.." EXPORT_DIR="$EXPORT_DIR" python3 - <<'PY'
import os, json, csv

def convert(src: str, dst: str) -> None:
    if not os.path.exists(src):
        return
    with open(src, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    if not data:
        return
    with open(dst, 'w', newline='', encoding='utf-8') as out:
        writer = csv.DictWriter(out, fieldnames=sorted(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)

export_dir = os.environ['EXPORT_DIR']
convert(os.path.join(export_dir, 'wifi.json'), os.path.join(export_dir, 'wifi.csv'))
convert(os.path.join(export_dir, 'bluetooth.json'), os.path.join(export_dir, 'bluetooth.csv'))
PY

echo "CSV files written to $EXPORT_DIR"
