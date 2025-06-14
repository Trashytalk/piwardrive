import subprocess
from typing import List, Dict

def scan_wifi(interface: str = "wlan0") -> List[Dict[str, str]]:
    """Scan for Wi-Fi networks using ``iwlist`` and return results."""
    cmd = ["sudo", "iwlist", interface, "scanning"]
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
    return networks
