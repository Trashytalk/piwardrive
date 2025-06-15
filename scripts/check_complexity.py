import logging
import subprocess
import sys

result = subprocess.run([
    'radon', 'cc', '-n', 'D', '-s', '.'
], capture_output=True, text=True)
logging.info(result.stdout)
if result.stdout.strip():
    logging.error("Complexity threshold exceeded")
    sys.exit(1)
