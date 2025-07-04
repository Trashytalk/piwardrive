import hashlib
import json

from piwardrive.analytics.iot import correlate_city_services, fingerprint_iot_devices


def test_fingerprint_iot_devices_basic() -> None:
    recs = [
        {
            "mac": "AA",
            "vendor": "Acme",
            "device_type": "camera",
            "protocols": ["http", "rtsp"],
            "firmware_version": "1.0",
        }
    ]
    rows = fingerprint_iot_devices(recs)
    assert rows and rows[0]["mac"] == "AA"  # nosec B101
    assert rows[0]["classification"] == "iot_sensor"
    char = {
        "vendor": "Acme",
        "device_type": "camera",
        "protocols": ["http", "rtsp"],
        "firmware_version": "1.0",
    }
    expected = hashlib.sha1(json.dumps(char, sort_keys=True).encode()).hexdigest()
    assert rows[0]["fingerprint_hash"] == expected


def test_correlate_city_services_window() -> None:
    events = [
        {"service": "water", "timestamp": 0},
        {"service": "power", "timestamp": 1},
        {"service": "water", "timestamp": 4},
        {"service": "power", "timestamp": 5},
    ]
    counts = correlate_city_services(events, window=2)
    assert counts[("power", "water")] == 2
