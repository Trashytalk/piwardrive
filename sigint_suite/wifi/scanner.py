import logging
import os
import shlex
import subprocess
from typing import List, Dict, Optional

from sigint_suite.models import WifiNetwork
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
    timeout: int | None = None,
) -> List[WifiNetwork]:

    """Scan for Wi-Fi networks using ``iwlist`` and return results."""

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
        output = subprocess.check_output(
            cmd, text=True, stderr=subprocess.DEVNULL, timeout=timeout
        )
    except Exception as exc:  # pragma: no cover - platform dependent
        logging.exception("Failed to run iwlist", exc_info=exc)
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
                current["bssid"] = line.split("Address:")[-1].strip()
        elif "ESSID" in line:
            current["ssid"] = line.split(":", 1)[-1].strip('"')
        elif "Address" in line:
            current["bssid"] = line.split("Address:")[-1].strip()
        elif "Frequency" in line:
            current["frequency"] = line.split("Frequency:")[-1].split(" ")[0]
        elif "Quality" in line:
            current["quality"] = line.split("Quality=")[-1].split(" ")[0]
    if current:
        networks.append(current)

    networks = apply_post_processors("wifi", networks)
    return [WifiNetwork(**rec) for rec in networks]



def main() -> None:
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


if __name__ == "__main__":
    main()
