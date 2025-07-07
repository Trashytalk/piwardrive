"""Security analysis helpers for suspicious Wi-Fi activity."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Iterable, List, Mapping

from piwardrive import persistence

_DEF_SEVERITY = {
    "evil_twin": "high",
    "deauth_attack": "medium",
    "hidden_ssid": "low",
}


def _make_row(
    activity_type: str,
    rec: Mapping[str, Any],
    evidence: Mapping[str, Any] | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    return {
        "scan_session_id": rec.get("scan_session_id", "adhoc"),
        "activity_type": activity_type,
        "severity": _DEF_SEVERITY.get(activity_type, "low"),
        "target_bssid": rec.get("bssid"),
        "target_ssid": rec.get("ssid"),
        "evidence": json.dumps(evidence or {}),
        "description": description,
        "detected_at": datetime.utcnow().isoformat(),
        "latitude": rec.get("latitude"),
        "longitude": rec.get("longitude"),
        "false_positive": False,
        "analyst_notes": None,
    }


def detect_hidden_ssids(records: Iterable[Mapping[str, Any]]) -> List[dict[str, Any]]:
    """Detect access points with hidden SSIDs.
    
    Args:
        records: WiFi detection records to analyze.
        
    Returns:
        List of suspicious activity records for hidden SSIDs.
    """
    rows: List[dict[str, Any]] = []
    for rec in records:
        if not rec.get("ssid"):
            rows.append(
                _make_row("hidden_ssid", rec, description="Hidden SSID detected")
            )
    return rows


def detect_evil_twins(records: Iterable[Mapping[str, Any]]) -> List[dict[str, Any]]:
    """Detect potential evil twin access points.
    
    Args:
        records: WiFi detection records to analyze.
        
    Returns:
        List of suspicious activity records for potential evil twins.
    """
    groups: dict[str, List[Mapping[str, Any]]] = {}
    for rec in records:
        ssid = rec.get("ssid") or ""
        groups.setdefault(ssid, []).append(rec)

    rows: List[dict[str, Any]] = []
    for ssid, items in groups.items():
        if not ssid or len(items) < 2:
            continue
        bssids = {i.get("bssid") for i in items if i.get("bssid")}
        if len(bssids) < 2:
            continue
        encs = {i.get("encryption_type") for i in items}
        vendors = {i.get("vendor_oui") for i in items}
        if len(encs) > 1 or len(vendors) > 1:
            evidence = {
                "bssids": list(bssids),
                "encryptions": list(encs),
                "vendors": list(vendors),
            }
            for rec in items:
                rows.append(
                    _make_row(
                        "evil_twin",
                        rec,
                        evidence=evidence,
                        description=f"Multiple APs broadcasting {ssid} with different properties",
                    )
                )
    return rows


def detect_deauth_attacks(records: Iterable[Mapping[str, Any]]) -> List[dict[str, Any]]:
    """Detect potential deauth attacks based on signal patterns.
    
    Args:
        records: WiFi detection records to analyze.
        
    Returns:
        List of suspicious activity records for potential deauth attacks.
    """
    rows: List[dict[str, Any]] = []
    for rec in records:
        if (
            rec.get("station_count") == 0
            and isinstance(rec.get("signal_strength_dbm"), (int, float))
            and rec.get("signal_strength_dbm") > -40
        ):
            rows.append(
                _make_row(
                    "deauth_attack",
                    rec,
                    description="Strong signal with zero clients may indicate deauth attack",
                )
            )
    return rows


async def analyze_wifi_records(records: Iterable[Mapping[str, Any]]) -> None:
    """Analyze Wi-Fi detection records and store suspicious activity rows."""
    rows: List[dict[str, Any]] = []
    records_list = list(records)
    rows.extend(detect_hidden_ssids(records_list))
    rows.extend(detect_evil_twins(records_list))
    rows.extend(detect_deauth_attacks(records_list))
    if rows:
        await persistence.save_suspicious_activities(rows)


__all__ = [
    "detect_hidden_ssids",
    "detect_evil_twins",
    "detect_deauth_attacks",
    "analyze_wifi_records",
]
