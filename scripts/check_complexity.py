import subprocess
import sys

result = subprocess.run([
    'radon', 'cc', '-n', 'D', '-s', '.'
], capture_output=True, text=True)
print(result.stdout)
if result.stdout.strip():
    print('Complexity threshold exceeded')
    sys.exit(1)
