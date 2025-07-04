import asyncio
from piwardrive.services import security_analyzer


def test_detect_hidden_ssids():
    records = [
        {
            "scan_session_id": "s1",
            "detection_timestamp": "2025-01-01T00:00:00",
            "ssid": "",
            "bssid": "AA:BB:CC:DD:EE:FF",
        }
    ]
    rows = security_analyzer.detect_hidden_ssids(records)
    assert rows and rows[0]["activity_type"] == "hidden_ssid"


def test_detect_evil_twins():
    recs = [
        {
            "scan_session_id": "s1",
            "detection_timestamp": "2025-01-01T00:00:00",
            "ssid": "Net",
            "bssid": "AA",
            "encryption_type": "WPA2",
            "vendor_oui": "AA",
        },
        {
            "scan_session_id": "s1",
            "detection_timestamp": "2025-01-01T00:00:01",
            "ssid": "Net",
            "bssid": "BB",
            "encryption_type": "WPA",
            "vendor_oui": "BB",
        },
    ]
    rows = security_analyzer.detect_evil_twins(recs)
    assert rows and rows[0]["activity_type"] == "evil_twin"
