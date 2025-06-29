import asyncio

from piwardrive.sigint_suite.wifi.scanner import async_scan_wifi, scan_wifi


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
    monkeypatch.setattr(
        "piwardrive.sigint_suite.wifi.scanner.lookup_vendor", _mock_lookup_vendor
    )
    monkeypatch.setattr(
        "piwardrive.sigint_suite.wifi.scanner.orientation_sensors.get_heading",
        lambda: 45.0,
    )

    nets = scan_wifi("wlan0")
    assert nets[0].vendor == "VendorA"
    assert nets[1].vendor == "VendorB"
    assert nets[0].channel == "6"
    assert nets[0].encryption == "on WPA Version 1"
    assert nets[1].channel == "3"
    assert nets[1].encryption == "off"
    assert nets[0].heading == 45.0


def test_scan_wifi_no_vendor(monkeypatch):
    output = """
Cell 01 - Address: AA:BB:CC:DD:EE:FF
          ESSID:"TestNet"
          Frequency:2.437 GHz (Channel 6)
          Encryption key:on
          Quality=70/70  Signal level=-40 dBm
"""
    monkeypatch.setattr("subprocess.check_output", lambda *a, **k: output)
    monkeypatch.setattr(
        "piwardrive.sigint_suite.wifi.scanner.lookup_vendor", lambda b: None
    )
    monkeypatch.setattr(
        "piwardrive.sigint_suite.wifi.scanner.orientation_sensors.get_heading",
        lambda: None,
    )

    nets = scan_wifi("wlan0")
    assert nets[0].vendor is None
    assert nets[0].channel == "6"
    assert nets[0].encryption == "on"
    assert nets[0].heading is None


def test_async_scan_wifi(monkeypatch):
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

    async def dummy_proc(*_a, **_k):
        class P:
            async def communicate(self):
                return (output.encode(), b"")

        return P()

    monkeypatch.setattr("asyncio.create_subprocess_exec", dummy_proc)
    monkeypatch.setattr(
        "piwardrive.sigint_suite.wifi.scanner.lookup_vendor", _mock_lookup_vendor
    )
    monkeypatch.setattr(
        "piwardrive.sigint_suite.wifi.scanner.orientation_sensors.get_heading",
        lambda: 90.0,
    )

    nets = asyncio.run(async_scan_wifi("wlan0"))
    assert nets[0].vendor == "VendorA"
    assert nets[1].vendor == "VendorB"
    assert nets[0].heading == 90.0
