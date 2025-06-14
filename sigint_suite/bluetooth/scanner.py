import subprocess
from typing import List, Dict


def scan_bluetooth(timeout: int = 10) -> List[Dict[str, str]]:
    """Scan for nearby Bluetooth devices using ``hcitool``."""
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
