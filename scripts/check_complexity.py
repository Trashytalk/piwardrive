import logging
import subprocess
import sys

try:
    result = subprocess.run(
        ['radon', 'cc', '-n', 'D', '-s', '.'],
        capture_output=True,
        text=True,
        check=True,
    )
except subprocess.CalledProcessError as exc:
    logging.error("Failed to run radon: %s", exc)
    sys.exit(1)
logging.info(result.stdout)
if result.stdout.strip():
    logging.error("Complexity threshold exceeded")
    sys.exit(1)
