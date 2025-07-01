import pytest

from piwardrive import network_analytics


@pytest.fixture(autouse=True)
def _mock_vendor_lookup(monkeypatch):
    """Provide deterministic vendor lookups for tests."""

    mapping = {
        "AA:BB:CC:DD:EE:FF": "V1",
        "11:22:33:44:55:66": "V2",
        "AA:AA:AA:AA:AA:AA": "V3",
        "BB:BB:BB:BB:BB:BB": "V4",
        "CC:DD:EE:FF:00:11": "V5",
        "DD:EE:FF:00:11:22": "V6",
        "AA:BB:CC:11:22:33": "V7",
    }

    def fake_lookup(bssid: str):
        return mapping.get(bssid)

    monkeypatch.setattr(network_analytics, "cached_lookup_vendor", fake_lookup)


def test_empty_records_returns_empty() -> None:
    assert network_analytics.find_suspicious_aps([]) == []  # nosec B101


def test_open_network_flagged() -> None:
    rec = {"bssid": "AA:BB:CC:DD:EE:FF", "ssid": "OpenNet", "encryption": "open"}
    assert network_analytics.find_suspicious_aps([rec]) == [rec]  # nosec B101


def test_duplicate_bssid_multiple_ssids_flagged_second_only() -> None:
    r1 = {"bssid": "11:22:33:44:55:66", "ssid": "Net1", "encryption": "wpa2"}
    r2 = {"bssid": "11:22:33:44:55:66", "ssid": "Net2", "encryption": "wpa2"}
    result = network_analytics.find_suspicious_aps([r1, r2])
    assert result == [r2]  # nosec B101


def test_missing_fields_handled() -> None:
    r1 = {"ssid": "Net", "encryption": "open"}
    r2 = {"bssid": "CC:DD:EE:FF:00:11"}
    result = network_analytics.find_suspicious_aps([r1, r2])
    assert result == [r1]  # nosec B101


def test_open_and_duplicate_combined() -> None:
    r1 = {"bssid": "AA:AA:AA:AA:AA:AA", "ssid": "Open1", "encryption": "open"}
    r2 = {"bssid": "AA:AA:AA:AA:AA:AA", "ssid": "Secure", "encryption": "wpa2"}
    r3 = {"bssid": "BB:BB:BB:BB:BB:BB", "ssid": "Other", "encryption": "wpa2"}
    result = network_analytics.find_suspicious_aps([r1, r2, r3])
    assert result == [r1, r2]  # nosec B101


def test_duplicate_bssid_same_ssid_not_flagged() -> None:
    r1 = {"bssid": "AA:BB:CC:11:22:33", "ssid": "Net", "encryption": "wpa2"}
    r2 = {"bssid": "AA:BB:CC:11:22:33", "ssid": "Net", "encryption": "wpa2"}
    result = network_analytics.find_suspicious_aps([r1, r2])
    assert result == []  # nosec B101


def test_wep_network_flagged() -> None:
    rec = {"bssid": "DD:EE:FF:00:11:22", "ssid": "OldNet", "encryption": "WEP"}
    assert network_analytics.find_suspicious_aps([rec]) == [rec]  # nosec B101


def test_unknown_vendor_flagged(monkeypatch) -> None:
    r = {"bssid": "12:34:56:78:9A:BC", "ssid": "Mystery", "encryption": "wpa2"}
    monkeypatch.setattr(network_analytics, "cached_lookup_vendor", lambda b: None)
    assert network_analytics.find_suspicious_aps([r]) == [r]  # nosec B101


def test_duplicate_bssid_three_ssids_flagged_second_third_only() -> None:
    r1 = {"bssid": "11:22:33:44:55:66", "ssid": "Net1", "encryption": "wpa2"}
    r2 = {"bssid": "11:22:33:44:55:66", "ssid": "Net2", "encryption": "wpa2"}
    r3 = {"bssid": "11:22:33:44:55:66", "ssid": "Net3", "encryption": "wpa2"}
    result = network_analytics.find_suspicious_aps([r1, r2, r3])
    assert result == [r2, r3]  # nosec B101


def test_open_network_case_insensitive() -> None:
    rec = {"bssid": "AA:BB:CC:DD:EE:FF", "ssid": "OpenNet", "encryption": "OPEN"}
    assert network_analytics.find_suspicious_aps([rec]) == [rec]  # nosec B101


def test_duplicate_and_unknown_vendor_flagged(monkeypatch) -> None:
    r1 = {"bssid": "00:11:22:33:44:55", "ssid": "Mystery1", "encryption": "wpa2"}
    r2 = {"bssid": "00:11:22:33:44:55", "ssid": "Mystery2", "encryption": "wpa2"}
    monkeypatch.setattr(network_analytics, "cached_lookup_vendor", lambda b: None)
    result = network_analytics.find_suspicious_aps([r1, r2])
    assert result == [r1, r2]  # nosec B101


def test_cluster_by_signal_returns_centroids() -> None:
    records = [
        {
            "bssid": "AA:BB:CC:11:22:33",
            "lat": 1.0,
            "lon": 1.0,
            "signal_dbm": -30,
        },
        {
            "bssid": "AA:BB:CC:11:22:33",
            "lat": 1.001,
            "lon": 1.001,
            "signal_dbm": -40,
        },
        {
            "bssid": "AA:BB:CC:11:22:33",
            "lat": 5.0,
            "lon": 5.0,
            "signal_dbm": -50,
        },
        {
            "bssid": "11:22:33:44:55:66",
            "lat": 2.0,
            "lon": 2.0,
            "signal_dbm": -20,
        },
        {
            "bssid": "11:22:33:44:55:66",
            "lat": 2.001,
            "lon": 2.001,
            "signal_dbm": -20,
        },
    ]

    centers = network_analytics.cluster_by_signal(records, eps=0.002, min_samples=2)
    a_lat, a_lon = centers["AA:BB:CC:11:22:33"]
    b_lat, b_lon = centers["11:22:33:44:55:66"]
    assert pytest.approx(a_lat, rel=1e-3) == 1.0004  # nosec B101
    assert pytest.approx(a_lon, rel=1e-3) == 1.0004  # nosec B101
    assert pytest.approx(b_lat, rel=1e-3) == 2.0005  # nosec B101
    assert pytest.approx(b_lon, rel=1e-3) == 2.0005  # nosec B101


def test_detect_rogue_devices_combines_checks() -> None:
    records = [
        {
            "bssid": "AA:BB:CC:11:22:33",
            "ssid": "Home",
            "encryption": "wpa2",
            "lat": 1.0,
            "lon": 1.0,
            "signal_dbm": -30,
        },
        {
            "bssid": "AA:BB:CC:11:22:33",
            "ssid": "Home",
            "encryption": "wpa2",
            "lat": 1.001,
            "lon": 1.001,
            "signal_dbm": -40,
        },
        {
            "bssid": "AA:BB:CC:11:22:33",
            "ssid": "Home",
            "encryption": "wpa2",
            "lat": 3.0,
            "lon": 3.0,
            "signal_dbm": -30,
        },
        {
            "bssid": "CC:DD:EE:FF:00:11",
            "ssid": "OpenNet",
            "encryption": "open",
            "lat": 0.0,
            "lon": 0.0,
            "signal_dbm": -50,
        },
    ]

    rogues = network_analytics.detect_rogue_devices(records, eps=0.002, min_samples=2, distance=0.001)
    assert records[2] in rogues  # nosec B101
    assert records[3] in rogues  # nosec B101
