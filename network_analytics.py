"""Advanced network analytics utilities."""

from __future__ import annotations

from typing import Iterable, Mapping, Any, List


def find_suspicious_aps(records: Iterable[Mapping[str, Any]]) -> List[Mapping[str, Any]]:
    """Return Wi-Fi access points that may be suspicious.

    Simple heuristics flag open networks or duplicate BSSIDs broadcasting
    multiple SSIDs.
    """
    aps: List[Mapping[str, Any]] = []
    seen_bssid: dict[str, set[str]] = {}
    for rec in records:
        bssid = rec.get("bssid")
        ssid = rec.get("ssid") or ""
        enc = rec.get("encryption") or ""
        if enc.lower() == "open":
            aps.append(rec)
        if bssid:
            seen_bssid.setdefault(bssid, set()).add(ssid)
            if len(seen_bssid[bssid]) > 1:
                aps.append(rec)
    return aps
