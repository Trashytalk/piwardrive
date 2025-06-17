import asyncio
import logging
import os
import subprocess
from typing import Dict, List

import contextlib
import logging


from sigint_suite.models import BluetoothDevice

logger = logging.getLogger(__name__)

_proc: asyncio.subprocess.Process | None = None
_reader_task: asyncio.Task | None = None
_devices: Dict[str, str] = {}


async def _reader() -> None:
    """Continuously parse ``bluetoothctl`` output."""
    assert _proc is not None and _proc.stdout is not None
    while True:
        line = await _proc.stdout.readline()
        if not line:
            break
        text = line.decode().strip()
        if "Device" in text and ":" in text:
            parts = text.split()
            try:
                idx = parts.index("Device")
            except ValueError:
                continue
            if idx + 1 < len(parts):
                addr = parts[idx + 1]
                name = " ".join(parts[idx + 2:]) if idx + 2 < len(parts) else addr
                _devices[addr] = name


async def start_scanner() -> None:
    """Launch ``bluetoothctl`` in interactive mode if not already running."""
    global _proc, _reader_task
    if _proc is not None and _proc.returncode is None:
        return
    _proc = await asyncio.create_subprocess_exec(
        "bluetoothctl",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
    )
    assert _proc.stdin is not None
    _proc.stdin.write(b"scan on\n")
    await _proc.stdin.drain()
    _reader_task = asyncio.create_task(_reader())


async def stop_scanner() -> None:
    """Terminate the background ``bluetoothctl`` process."""
    global _proc, _reader_task, _devices
    if _proc is None:
        return
    try:
        if _proc.stdin:
            _proc.stdin.write(b"scan off\n")
            await _proc.stdin.drain()
    except Exception:
        pass
    if _reader_task:
        _reader_task.cancel()
        with contextlib.suppress(Exception):
            await _reader_task
    with contextlib.suppress(Exception):
        _proc.terminate()
        await asyncio.wait_for(_proc.wait(), timeout=2.0)
    _proc = None
    _reader_task = None
    _devices = {}

def scan_bluetooth(timeout: int = 10) -> List[BluetoothDevice]:
    """Scan for nearby Bluetooth devices using ``bleak`` or ``bluetoothctl``."""
    timeout = (
        timeout
        if timeout is not None
        else int(os.getenv("BLUETOOTH_SCAN_TIMEOUT", "10"))
    )
    try:
        return asyncio.run(async_scan_bluetooth(timeout))
    except Exception:
        return _scan_bluetoothctl(timeout)




async def async_scan_bluetooth(timeout: int = 10) -> List[BluetoothDevice]:
    """Asynchronously scan for nearby Bluetooth devices."""
    timeout = (
        timeout
        if timeout is not None
        else int(os.getenv("BLUETOOTH_SCAN_TIMEOUT", "10"))
    )
    try:
        from bleak import BleakScanner  # type: ignore

        found = await BleakScanner.discover(timeout=timeout)
        return [
            {"address": dev.address, "name": dev.name or dev.address}
            for dev in found
        ]
    except Exception:
        pass

    await start_scanner()
    await asyncio.sleep(timeout)
    return [BluetoothDevice(address=a, name=n) for a, n in _devices.items()]


def _scan_bluetoothctl(timeout: int) -> List[Dict[str, str]]:

    """Scan using ``bluetoothctl`` as a fallback."""
    cmd = ["bluetoothctl", "--timeout", str(timeout), "scan", "on"]
    logger.debug("Executing: %s", " ".join(cmd))
    try:
        output = subprocess.check_output(cmd, text=True)
    except Exception as exc:  # pragma: no cover - external command
        logger.exception("Bluetooth scan failed: %s", exc)
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

    devices: Dict[str, str] = {}
    for line in output.splitlines():
        if "Device" in line and ":" in line:
            parts = line.split()
            try:
                idx = parts.index("Device")
            except ValueError:
                continue
            if idx + 1 < len(parts):
                addr = parts[idx + 1]
                name = " ".join(parts[idx + 2 :]) if idx + 2 < len(parts) else addr
                devices[addr] = name
    return [BluetoothDevice(address=a, name=n) for a, n in devices.items()]


def main() -> None:  # pragma: no cover - CLI helper

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
        for dev in devices:
            print(f"{dev.address} {dev.name}")


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
