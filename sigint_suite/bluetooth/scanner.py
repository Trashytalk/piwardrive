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


def main() -> None:
    """Command-line interface for Bluetooth scanning."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Scan for Bluetooth devices")
    parser.add_argument("--timeout", type=int, default=10, help="scan timeout")
    parser.add_argument("--json", action="store_true", help="print results as JSON")
    args = parser.parse_args()

    devices = scan_bluetooth(args.timeout)
    if args.json:
        print(json.dumps(devices, indent=2))
    else:
        for rec in devices:
            print(f"{rec['address']} {rec['name']}")


if __name__ == "__main__":
    main()
