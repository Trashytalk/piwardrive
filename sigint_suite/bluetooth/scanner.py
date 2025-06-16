import os
import subprocess
from typing import List, Dict


def scan_bluetooth(timeout: int | None = None) -> List[Dict[str, str]]:
    """Scan for nearby Bluetooth devices using ``hcitool``."""
    timeout = timeout if timeout is not None else int(os.getenv("BLUETOOTH_SCAN_TIMEOUT", "10"))
    cmd = ["hcitool", "scan"]
    try:
        output = subprocess.check_output(cmd, text=True, timeout=timeout)
    except Exception:
        return []

    devices: List[Dict[str, str]] = []
    for line in output.splitlines():
        if ":" in line:
            parts = line.split()
            if len(parts) >= 2:
                addr = parts[0]
                name = " ".join(parts[1:])
                devices.append({"address": addr, "name": name})
    return devices
