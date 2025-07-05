from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Iterable, List, Mapping, Tuple


def _extract_features(rec: Mapping[str, Any]) -> Dict[str, Any]:
    fields = ["vendor", "device_type", "protocols", "firmware_version"]
    feat: Dict[str, Any] = {}
    for field in fields:
        val = rec.get(field)
        if val:
            if field == "protocols" and isinstance(val, list):
                feat[field] = sorted(val)
            else:
                feat[field] = val
    return feat


def _hash_features(feat: Mapping[str, Any]) -> str:
    data = json.dumps(feat, sort_keys=True).encode()
    return hashlib.sha256(data).hexdigest()


def _classify(rec: Mapping[str, Any]) -> Tuple[str, str]:
    dtype = str(rec.get("device_type") or "").lower()
    if dtype in {"camera", "sensor"}:
        return "iot_sensor", "low"
    if dtype in {"thermostat", "appliance"}:
        return "smart_appliance", "medium"
    return "generic", "low"


def fingerprint_iot_devices(
    records: Iterable[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    """Return fingerprint rows for IoT device ``records``."""
    rows: List[Dict[str, Any]] = []
    for rec in records:
        mac = rec.get("mac")
        if not mac:
            continue
        feat = _extract_features(rec)
        fp_hash = _hash_features(feat)
        cls, risk = _classify(rec)
        rows.append(
            {
                "mac": mac,
                "fingerprint_hash": fp_hash,
                "classification": cls,
                "risk_level": risk,
                "characteristics": json.dumps(feat),
            }
        )
    return rows


def correlate_city_services(
    events: Iterable[Mapping[str, Any]], window: int = 300
) -> Dict[Tuple[str, str], int]:
    """Count co-occurring service events within ``window`` seconds."""
    items = [
        (str(e.get("service")), float(e.get("timestamp", 0)))
        for e in events
        if e.get("service") is not None
    ]
    items.sort(key=lambda x: x[1])
    counts: Dict[Tuple[str, str], int] = {}
    for i, (svc_i, ts_i) in enumerate(items):
        for svc_j, ts_j in items[i + 1 :]:
            if ts_j - ts_i > window:
                break
            pair = tuple(sorted((svc_i, svc_j)))
            counts[pair] = counts.get(pair, 0) + 1
    return counts


__all__ = ["fingerprint_iot_devices", "correlate_city_services"]
