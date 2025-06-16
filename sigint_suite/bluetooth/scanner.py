import os

"""Bluetooth scanning helpers using modern tools."""

import asyncio

import subprocess
from typing import List
import logging

logger = logging.getLogger(__name__)


from sigint_suite.models import BluetoothDevice


def scan_bluetooth(timeout: int = 10) -> List[BluetoothDevice]:

    """Scan for nearby Bluetooth devices using ``hcitool``."""
    timeout = timeout if timeout is not None else int(os.getenv("BLUETOOTH_SCAN_TIMEOUT", "10"))
    cmd = ["hcitool", "scan"]
    logger.debug("Scanning bluetooth with timeout %s", timeout)

    try:
        from bleak import BleakScanner  # type: ignore

        async def _scan() -> List[Dict[str, str]]:
            found = await BleakScanner.discover(timeout=timeout)
            return [
                {"address": dev.address, "name": dev.name or dev.address}
                for dev in found
            ]

        return asyncio.run(_scan())
    except Exception as exc:
        logger.debug("Bleak unavailable or failed: %s", exc)
        pass

    return _scan_bluetoothctl(timeout)


def _scan_bluetoothctl(timeout: int) -> List[Dict[str, str]]:
    """Scan using ``bluetoothctl`` as a fallback."""

    cmd = ["bluetoothctl", "--timeout", str(timeout), "scan", "on"]
    logger.debug("Executing: %s", " ".join(cmd))
    try:
        output = subprocess.check_output(cmd, text=True)
    except Exception as exc:
        logger.exception("Bluetooth scan failed: %s", exc)
        return []

    devices: List[BluetoothDevice] = []
    for line in output.splitlines():
        if "Device" in line and ":" in line:
            parts = line.split()
            if len(parts) >= 2:
                addr = parts[0]
                name = " ".join(parts[1:])
                devices.append(BluetoothDevice(address=addr, name=name))
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
            try:
                idx = parts.index("Device")
            except ValueError:
                continue
            if idx + 1 < len(parts):
                addr = parts[idx + 1]
                name = " ".join(parts[idx + 2:]) if idx + 2 < len(parts) else addr
                devices[addr] = name

    return [{"address": a, "name": n} for a, n in devices.items()]
