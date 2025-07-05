from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable

from piwardrive import persistence


def _extract_characteristics(record: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "vendor_oui",
        "vendor_name",
        "encryption_type",
        "cipher_suite",
        "authentication_method",
        "beacon_interval_ms",
        "dtim_period",
        "ht_capabilities",
        "vht_capabilities",
        "he_capabilities",
        "country_code",
        "regulatory_domain",
        "channel",
        "frequency_mhz",
        "tx_power_dbm",
        "device_type",
    ]
    return {k: record.get(k) for k in keys if record.get(k) is not None}


def _classify(record: dict[str, Any]) -> tuple[str, str]:
    enc = (record.get("encryption_type") or "").upper()
    vendor = (record.get("vendor_name") or "").lower()
    if enc in {"", "OPEN"}:
        classification = "public"
        risk = "medium"
    elif "CISCO" in vendor or "ubiquiti" in vendor:
        classification = "business"
        risk = "low"
    else:
        classification = "home"
        risk = "low"
    if "WEP" in enc:
        risk = "high"
    return classification, risk


def _fingerprint_hash(char: dict[str, Any]) -> str:
    data = json.dumps(char, sort_keys=True).encode()
    return hashlib.sha256(data).hexdigest()


def _make_row(record: dict[str, Any]) -> dict[str, Any]:
    char = _extract_characteristics(record)
    fp_hash = _fingerprint_hash(char)
    classification, risk = _classify(record)
    confidence = min(1.0, len(char) / 10.0)
    return {
        "bssid": record.get("bssid"),
        "ssid": record.get("ssid"),
        "fingerprint_hash": fp_hash,
        "confidence_score": confidence,
        "device_model": None,
        "firmware_version": None,
        "characteristics": json.dumps(char),
        "classification": classification,
        "risk_level": risk,
        "tags": json.dumps(list(char.keys())),
    }


async def fingerprint_wifi_records(records: Iterable[dict[str, Any]]) -> None:
    """Generate fingerprints for Wi-Fi detection ``records``."""
    rows = [_make_row(r) for r in records if r.get("bssid")]
    if rows:
        await persistence.save_network_fingerprints(rows)
