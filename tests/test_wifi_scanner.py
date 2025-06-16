import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sigint_suite.wifi.scanner import scan_wifi


def _mock_lookup_vendor(bssid: str):
    mapping = {
        "AA:BB:CC": "VendorA",
        "11:22:33": "VendorB",
    }
    return mapping.get(bssid[:8])


def test_scan_wifi_enriches_vendor(monkeypatch):
    output = """
Cell 01 - Address: AA:BB:CC:DD:EE:FF
          ESSID:"TestNet"
          Frequency:2.437 GHz (Channel 6)
          Encryption key:on
          IE: WPA Version 1
          Quality=70/70  Signal level=-40 dBm
Cell 02 - Address: 11:22:33:44:55:66
          ESSID:"OpenNet"
          Frequency:2.422 GHz (Channel 3)
          Encryption key:off
          Quality=20/70  Signal level=-90 dBm
"""
    monkeypatch.setattr("subprocess.check_output", lambda *a, **k: output)
    monkeypatch.setattr("sigint_suite.wifi.scanner.lookup_vendor", _mock_lookup_vendor)

    nets = scan_wifi("wlan0")
    assert nets[0].vendor == "VendorA"
    assert nets[1].vendor == "VendorB"
    assert nets[0].channel == "6"
    assert nets[0].encryption == "on WPA Version 1"
    assert nets[1].channel == "3"
    assert nets[1].encryption == "off"


def test_scan_wifi_no_vendor(monkeypatch):
    output = """
Cell 01 - Address: AA:BB:CC:DD:EE:FF
          ESSID:"TestNet"
          Frequency:2.437 GHz (Channel 6)
          Encryption key:on
          Quality=70/70  Signal level=-40 dBm
"""
    monkeypatch.setattr("subprocess.check_output", lambda *a, **k: output)
    monkeypatch.setattr("sigint_suite.wifi.scanner.lookup_vendor", lambda b: None)

    nets = scan_wifi("wlan0")
    assert nets[0].vendor is None
    assert nets[0].channel == "6"
    assert nets[0].encryption == "on"
