"""Wi-Fi scanning utilities."""

from __future__ import annotations

import asyncio
import logging
import os
import shlex
import subprocess
from typing import Dict, Iterable, List, Optional, Union

from piwardrive import orientation_sensors
from piwardrive.sigint_suite.enrichment import cached_lookup_vendor
from piwardrive.sigint_suite.hooks import (apply_post_processors,
                                           register_post_processor)
from piwardrive.sigint_suite.models import WifiNetwork

logger = logging.getLogger(__name__)

# expose lookup_vendor for tests, defaulting to cached_lookup_vendor
lookup_vendor = cached_lookup_vendor


def _vendor_hook(
    records: List[Dict[str, Union[str, float]]],
) -> List[Dict[str, Union[str, float]]]:
    """Add vendor names based on BSSID prefixes."""
    for rec in records:
        bssid = rec.get("bssid")
        vendor = cached_lookup_vendor(bssid)
        if vendor:
            rec["vendor"] = vendor
    return records


register_post_processor("wifi", _vendor_hook)


def _parse_iwlist_output(
    output: str,
    heading: float | None,
) -> Iterable[Dict[str, str]]:
    """Yield dictionaries parsed from ``iwlist`` command output."""
    current: Dict[str, str] = {}
    enc_lines: List[str] = []
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("Cell"):
            if current:
                if heading is not None:
                    current["heading"] = heading
                if enc_lines:
                    enc = " ".join(enc_lines).strip()
                    if "encryption" in current:
                        current["encryption"] = f"{current['encryption']} {enc}".strip()
                    else:
                        current["encryption"] = enc
                yield current
            bssid = None
            if "Address:" in line:
                bssid = line.split("Address:")[-1].strip()
            current = {"cell": line}
            if bssid:
                current["bssid"] = bssid
            enc_lines = []
        elif "ESSID" in line:
            current["ssid"] = line.split(":", 1)[-1].strip('"')
        elif line.startswith("Encryption key:"):
            current["encryption"] = line.split("Encryption key:")[-1].strip()
        elif line.startswith("IE:"):
            enc_lines.append(line.split("IE:", 1)[-1].strip())
        elif "Address" in line:
            current["bssid"] = line.split("Address:")[-1].strip()
        elif "Frequency" in line:
            current["frequency"] = line.split("Frequency:")[-1].split()[0]
            if "(Channel" in line:
                ch = line.split("(Channel")[-1].split(")")[0].strip()
                current["channel"] = ch
        elif line.startswith("Channel:"):
            current["channel"] = line.split("Channel:")[-1].strip()
        elif "Quality" in line:
            current["quality"] = line.split("Quality=")[-1].split()[0]
    if current:
        if heading is not None:
            current["heading"] = heading
        if enc_lines:
            enc = " ".join(enc_lines).strip()
            if "encryption" in current:
                current["encryption"] = f"{current['encryption']} {enc}".strip()
            else:
                current["encryption"] = enc
        yield current


def scan_wifi(
    interface: str = "wlan0",
    iwlist_cmd: Optional[str] = None,
    priv_cmd: Optional[str] = None,
    timeout: Optional[int] = None,
) -> List[WifiNetwork]:
    """Scan for Wi-Fi networks using ``iwlist`` and return results."""
    iwlist_cmd = str(iwlist_cmd or os.getenv("IWLIST_CMD", "iwlist"))
    priv_cmd = priv_cmd if priv_cmd is not None else os.getenv("IW_PRIV_CMD", "sudo")

    cmd: List[str] = []
    if priv_cmd:
        cmd.extend(shlex.split(priv_cmd))
    cmd.extend([iwlist_cmd, interface, "scanning"])
    timeout = (
        timeout if timeout is not None else int(os.getenv("WIFI_SCAN_TIMEOUT", "10"))
    )

    try:
        output = subprocess.check_output(
            cmd,
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
        )
    except Exception as exc:  # pragma: no cover - external command
        logger.exception("Wi-Fi scan failed: %s", exc)
        return []

    heading = orientation_sensors.get_heading()
    records = list(_parse_iwlist_output(output, heading))
    records = apply_post_processors("wifi", records)
    return [WifiNetwork(**rec) for rec in records]


async def async_scan_wifi(
    interface: str = "wlan0",
    iwlist_cmd: Optional[str] = None,
    priv_cmd: Optional[str] = None,
    timeout: int | None = None,
) -> List[WifiNetwork]:
    """Asynchronously scan for Wi-Fi networks using ``iwlist``."""
    iwlist_cmd = iwlist_cmd or os.getenv("IWLIST_CMD", "iwlist")
    priv_cmd = priv_cmd if priv_cmd is not None else os.getenv("IW_PRIV_CMD", "sudo")

    cmd: List[str] = []
    if priv_cmd:
        cmd.extend(shlex.split(priv_cmd))
    cmd.extend([iwlist_cmd, interface, "scanning"])
    timeout = (
        timeout if timeout is not None else int(os.getenv("WIFI_SCAN_TIMEOUT", "10"))
    )
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        output = stdout.decode()
    except Exception:  # pragma: no cover - external command
        return []

    heading = orientation_sensors.get_heading()
    records = list(_parse_iwlist_output(output, heading))
    records = apply_post_processors("wifi", records)
    return [WifiNetwork(**rec) for rec in records]


def main() -> None:  # pragma: no cover - CLI helper
    """Command-line interface for Wi-Fi scanning."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Scan for Wi-Fi networks")
    parser.add_argument("--interface", default="wlan0", help="wireless interface")
    parser.add_argument("--json", action="store_true", help="print results as JSON")
    args = parser.parse_args()

    nets = scan_wifi(args.interface)
    if args.json:
        print(json.dumps([n.model_dump() for n in nets], indent=2))
    else:
        for rec in nets:
            ssid = rec.ssid or ""
            bssid = rec.bssid or ""
            print(f"{ssid} {bssid}")


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
