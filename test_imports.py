"""
Simple diagnostic test to check for import hangs.
"""

import sys
import time
import signal

def timeout_handler(signum, frame):
    print(f"Import timeout after 10 seconds")
    sys.exit(1)

# Set a timeout for imports
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)

try:
    print("Testing basic imports...")
    
    print("1. Testing config import...")
    from piwardrive.core.config import Config
    print("✓ Core config imported")
    
    print("2. Testing persistence import...")
    from piwardrive.core.persistence import AppState
    print("✓ Core persistence imported")
    
    print("3. Testing main app import...")
    from piwardrive.main import PiWardriveApp
    print("✓ PiWardriveApp imported")
    
    print("All imports successful!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Unexpected error: {e}")
finally:
    signal.alarm(0)  # Cancel the alarm
