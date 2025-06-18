import os
import sys


from piwardrive import network_analytics


def test_empty_records_returns_empty() -> None:
    assert network_analytics.find_suspicious_aps([]) == []


def test_open_network_flagged() -> None:
    rec = {"bssid": "AA:BB:CC:DD:EE:FF", "ssid": "OpenNet", "encryption": "open"}
    assert network_analytics.find_suspicious_aps([rec]) == [rec]


def test_duplicate_bssid_multiple_ssids_flagged_second_only() -> None:
    r1 = {"bssid": "11:22:33:44:55:66", "ssid": "Net1", "encryption": "wpa2"}
    r2 = {"bssid": "11:22:33:44:55:66", "ssid": "Net2", "encryption": "wpa2"}
    result = network_analytics.find_suspicious_aps([r1, r2])
    assert result == [r2]


def test_missing_fields_handled() -> None:
    r1 = {"ssid": "Net", "encryption": "open"}
    r2 = {"bssid": "CC:DD:EE:FF:00:11"}
    result = network_analytics.find_suspicious_aps([r1, r2])
    assert result == [r1]


def test_open_and_duplicate_combined() -> None:
    r1 = {"bssid": "AA:AA:AA:AA:AA:AA", "ssid": "Open1", "encryption": "open"}
    r2 = {"bssid": "AA:AA:AA:AA:AA:AA", "ssid": "Secure", "encryption": "wpa2"}
    r3 = {"bssid": "BB:BB:BB:BB:BB:BB", "ssid": "Other", "encryption": "wpa2"}
    result = network_analytics.find_suspicious_aps([r1, r2, r3])
    assert result == [r1, r2]
