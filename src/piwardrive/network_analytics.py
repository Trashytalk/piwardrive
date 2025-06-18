"""Advanced network analytics utilities."""

from __future__ import annotations

from typing import Iterable, Mapping, Any, List

from piwardrive.sigint_suite.enrichment import cached_lookup_vendor


def find_suspicious_aps(
    records: Iterable[Mapping[str, Any]]
) -> List[Mapping[str, Any]]:
    """Return Wi-Fi access points that may be suspicious.

    Heuristics flag open or WEP networks, duplicate BSSIDs broadcasting
    multiple SSIDs, out-of-range channels and unknown vendor prefixes.
    """
    aps: List[Mapping[str, Any]] = []
    seen_bssid: dict[str, set[str]] = {}
    for rec in records:
        bssid = rec.get("bssid")
        ssid = rec.get("ssid") or ""
        enc = (rec.get("encryption") or "").lower()
        channel = rec.get("channel")

        suspicious = False
        if "open" in enc or "wep" in enc:
            suspicious = True
        if bssid:
            seen_bssid.setdefault(bssid, set()).add(ssid)
            if len(seen_bssid[bssid]) > 1:
                suspicious = True
        if channel not in (None, ""):
            try:
                ch = int(str(channel).split()[0])
                if ch < 1 or ch > 196:
                    suspicious = True
            except ValueError:
                suspicious = True
        if bssid and cached_lookup_vendor(bssid) is None:
            suspicious = True

        if suspicious:
            aps.append(rec)
    return aps
