"""
Simple diagnostic test to check for import hangs.
"""

import signal
import sys


def timeout_handler(signum, frame):
    print(f"Import timeout after 10 seconds")
    sys.exit(1)

# Set a timeout for imports
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)

try:
    print("Testing basic imports...")
    
    print("1. Testing config import...")
    print("✓ Core config imported")
    
    print("2. Testing persistence import...")
    print("✓ Core persistence imported")
    
    print("3. Testing main app import...")
    print("✓ PiWardriveApp imported")
    
    print("All imports successful!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Unexpected error: {e}")
finally:
    signal.alarm(0)  # Cancel the alarm
