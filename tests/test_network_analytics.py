import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import network_analytics as na


def test_find_suspicious_aps(monkeypatch):
    records = [
        {"bssid": "00:11:22:33:44:55", "ssid": "OpenNet", "encryption": "OPEN"},
        {"bssid": "AA:AA:AA:AA:AA:AA", "ssid": "Test1", "encryption": "WPA2"},
        {"bssid": "AA:AA:AA:AA:AA:AA", "ssid": "Test2", "encryption": "WPA2"},
        {"bssid": "BB:BB:BB:BB:BB:BB", "ssid": "WepNet", "encryption": "WEP"},
        {
            "bssid": "CC:CC:CC:CC:CC:CC",
            "ssid": "BadChannel",
            "encryption": "WPA2",
            "channel": "300",
        },
        {"bssid": "CC:DD:EE:FF:00:11", "ssid": "Unknown", "encryption": "WPA2"},
    ]

    def lookup(bssid: str):
        return None if bssid == "CC:DD:EE:FF:00:11" else "V"

    monkeypatch.setattr(na, "lookup_vendor", lookup)

    suspicious = na.find_suspicious_aps(records)
    assert len(suspicious) == 5
    assert records[0] in suspicious
    assert records[2] in suspicious  # duplicate SSID
    assert records[3] in suspicious
    assert records[4] in suspicious
    assert records[5] in suspicious
