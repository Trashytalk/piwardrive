"""Bluetooth scanning helpers using modern tools."""

import asyncio
import logging
import os
import subprocess
from typing import List

from sigint_suite.models import BluetoothDevice


def scan_bluetooth(timeout: int = 10) -> List[BluetoothDevice]:
    """Scan for nearby Bluetooth devices."""
    timeout = timeout if timeout is not None else int(os.getenv("BLUETOOTH_SCAN_TIMEOUT", "10"))

    try:
        from bleak import BleakScanner  # type: ignore

        async def _scan() -> List[BluetoothDevice]:
            found = await BleakScanner.discover(timeout=timeout)
            return [
                BluetoothDevice(address=dev.address, name=dev.name or dev.address)
                for dev in found
            ]

        return asyncio.run(_scan())
    except Exception:
        pass

    return _scan_bluetoothctl(timeout)


async def async_scan_bluetooth(timeout: int = 10) -> List[BluetoothDevice]:
    """Asynchronously scan for nearby Bluetooth devices."""

    timeout = timeout if timeout is not None else int(os.getenv("BLUETOOTH_SCAN_TIMEOUT", "10"))

    try:
        from bleak import BleakScanner  # type: ignore

        found = await BleakScanner.discover(timeout=timeout)
        return [
            {"address": dev.address, "name": dev.name or dev.address}
            for dev in found
        ]
    except Exception:
        pass

    return await _async_scan_bluetoothctl(timeout)


def _scan_bluetoothctl(timeout: int) -> List[Dict[str, str]]:

    """Scan using ``bluetoothctl`` as a fallback."""

    cmd = ["bluetoothctl", "--timeout", str(timeout), "scan", "on"]
    try:
        output = subprocess.check_output(cmd, text=True)
    except Exception as exc:  # pragma: no cover - external command
        logging.exception("Failed to run bluetoothctl", exc_info=exc)
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



async def _async_scan_bluetoothctl(timeout: int) -> List[Dict[str, str]]:
    """Async wrapper for ``bluetoothctl``."""

    cmd = ["bluetoothctl", "--timeout", str(timeout), "scan", "on"]
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout + 1)
        output = stdout.decode()
    except Exception:
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
        print(json.dumps([d.model_dump() for d in devices], indent=2))
    else:
        for rec in devices:
            print(f"{rec.address} {rec.name}")


if __name__ == "__main__":
    main()
