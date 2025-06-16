import csv
import os
from functools import lru_cache
from typing import Dict, Optional

OUI_PATH = os.path.join(os.path.dirname(__file__), "oui.csv")


def load_oui_map(path: str = OUI_PATH) -> Dict[str, str]:
    """Return a mapping of MAC prefixes to vendor names."""
    mapping: Dict[str, str] = {}
    if not os.path.exists(path):
        return mapping
    with open(path, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            assignment = (row.get("Assignment") or "").strip()
            vendor = (row.get("Organization Name") or "").strip()
            if assignment and vendor:
                prefix = assignment.replace("-", ":").upper()
                mapping[prefix] = vendor
    return mapping


@lru_cache(maxsize=1)
def _default_map() -> Dict[str, str]:
    return load_oui_map()


def lookup_vendor(
    bssid: str, oui_map: Optional[Dict[str, str]] = None
) -> Optional[str]:
    """Return vendor name for ``bssid`` if known."""
    if not bssid:
        return None
    bssid = bssid.upper().replace('-', ':')
    parts = bssid.split(':')
    if len(parts) < 3:
        return None
    prefix = ':'.join(parts[:3])
    return (oui_map or _default_map()).get(prefix)


__all__ = ["load_oui_map", "lookup_vendor"]
