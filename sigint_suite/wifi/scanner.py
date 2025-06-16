import os
import shlex
import subprocess
from typing import List, Dict, Optional

from sigint_suite.enrichment import lookup_vendor
from sigint_suite.hooks import apply_post_processors, register_post_processor


def _vendor_hook(records: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Add vendor names based on BSSID prefixes."""
    for rec in records:
        bssid = rec.get("bssid")
        vendor = lookup_vendor(bssid)
        if vendor:
            rec["vendor"] = vendor
    return records


register_post_processor("wifi", _vendor_hook)


def scan_wifi(
    interface: str = "wlan0",
    iwlist_cmd: Optional[str] = None,
    priv_cmd: Optional[str] = None,
) -> List[Dict[str, str]]:
    """Scan for Wi-Fi networks using ``iwlist`` and return results."""

    iwlist_cmd = iwlist_cmd or os.getenv("IWLIST_CMD", "iwlist")
    priv_cmd = priv_cmd if priv_cmd is not None else os.getenv("IW_PRIV_CMD", "sudo")

    cmd: List[str] = []
    if priv_cmd:
        cmd.extend(shlex.split(priv_cmd))
    cmd.extend([iwlist_cmd, interface, "scanning"])
    try:
        output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return []

    networks: List[Dict[str, str]] = []
    current: Dict[str, str] = {}
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("Cell"):
            if current:
                networks.append(current)
            current = {"cell": line}
            if "Address:" in line:
                bssid = line.split("Address:")[-1].strip()
                current["bssid"] = bssid
        elif "ESSID" in line:
            current["ssid"] = line.split(":", 1)[-1].strip('"')
        elif "Address" in line:
            bssid = line.split("Address:")[-1].strip()
            current["bssid"] = bssid
        elif "Frequency" in line:
            current["frequency"] = line.split("Frequency:")[-1].split(" ")[0]
        elif "Quality" in line:
            current["quality"] = line.split("Quality=")[-1].split(" ")[0]
    if current:
        networks.append(current)
    networks = apply_post_processors("wifi", networks)
    return networks
