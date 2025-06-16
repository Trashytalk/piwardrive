import os

"""Bluetooth scanning helpers using modern tools."""

import asyncio
import subprocess
from typing import Dict, List


def scan_bluetooth(timeout: int = 10) -> List[Dict[str, str]]:

    """Scan for nearby Bluetooth devices using ``hcitool``."""
    timeout = (
        timeout
        if timeout is not None
        else int(os.getenv("BLUETOOTH_SCAN_TIMEOUT", "10"))
    )

    try:
        from bleak import BleakScanner  # type: ignore

        async def _scan() -> List[Dict[str, str]]:
            found = await BleakScanner.discover(timeout=timeout)
            return [
                {"address": dev.address, "name": dev.name or dev.address}
                for dev in found
            ]

        return asyncio.run(_scan())
    except Exception:
        pass

    return _scan_bluetoothctl(timeout)


def _scan_bluetoothctl(timeout: int) -> List[Dict[str, str]]:
    """Scan using ``bluetoothctl`` as a fallback."""

    cmd = ["bluetoothctl", "--timeout", str(timeout), "scan", "on"]
    try:
        output = subprocess.check_output(cmd, text=True)
    except Exception:
        return []

    devices: Dict[str, str] = {}
    for line in output.splitlines():
        parts = line.split()
        try:
            idx = parts.index("Device")
        except ValueError:
            continue
        if idx + 1 < len(parts):
            addr = parts[idx + 1]
            name = " ".join(parts[idx + 2:]) if idx + 2 < len(parts) else addr
            devices[addr] = name

    return [{"address": a, "name": n} for a, n in devices.items()]


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
