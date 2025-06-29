import asyncio
from piwardrive.sigint_suite.wifi.scanner import _parse_iwlist_output, scan_wifi
from piwardrive.sigint_suite.bluetooth.scanner import (
    _scan_bluetoothctl,
    _async_scan_bluetoothctl,
)


WIFI_OUTPUT = """\
Cell 01 - Address: AA:BB:CC:DD:EE:FF
          ESSID:"TestNet"
          Frequency:2.437 GHz (Channel 6)
          Encryption key:on
          IE: WPA2
          Quality=70/70  Signal level=-40 dBm
Cell 02 - Address: 11:22:33:44:55:66
          ESSID:"OpenNet"
          Channel:11
          Quality=60/70  Signal level=-50 dBm
          Encryption key:off
"""

BT_OUTPUT = """\
[NEW] Device AA:BB:CC:DD:EE:FF DeviceOne
[NEW] Device 11:22:33:44:55:66 Another Device
"""


def test_parse_iwlist_output():
    records = list(_parse_iwlist_output(WIFI_OUTPUT, 12.3))
    assert records[0]["bssid"] == "AA:BB:CC:DD:EE:FF"
    assert records[0]["ssid"] == "TestNet"
    assert records[0]["frequency"] == "2.437"
    assert records[0]["channel"] == "6"
    assert records[0]["encryption"] == "on WPA2"
    assert records[0]["heading"] == 12.3
    assert records[1]["bssid"] == "11:22:33:44:55:66"
    assert records[1]["ssid"] == "OpenNet"
    assert records[1]["channel"] == "11"
    assert records[1]["encryption"] == "off"
    assert records[1]["heading"] == 12.3


def test_scan_wifi(monkeypatch):
    monkeypatch.setattr("subprocess.check_output", lambda *a, **k: WIFI_OUTPUT)
    monkeypatch.setattr(
        "piwardrive.sigint_suite.wifi.scanner.orientation_sensors.get_heading",
        lambda: 12.3,
    )
    monkeypatch.setattr(
        "piwardrive.sigint_suite.wifi.scanner.apply_post_processors", lambda t, r: r
    )
    nets = scan_wifi("wlan0")
    assert nets[0].ssid == "TestNet"
    assert nets[0].heading == 12.3
    assert nets[1].ssid == "OpenNet"


def test_scan_bluetoothctl(monkeypatch):
    monkeypatch.setattr("subprocess.check_output", lambda *a, **k: BT_OUTPUT)
    devices = _scan_bluetoothctl(2)
    assert devices == [
        {"address": "AA:BB:CC:DD:EE:FF", "name": "DeviceOne"},
        {"address": "11:22:33:44:55:66", "name": "Another Device"},
    ]


def test_async_scan_bluetoothctl(monkeypatch):
    async def fake_proc(*_a, **_k):
        class P:
            async def communicate(self):
                return (BT_OUTPUT.encode(), b"")

        return P()

    monkeypatch.setattr("asyncio.create_subprocess_exec", fake_proc)
    devices = asyncio.run(_async_scan_bluetoothctl(2))
    assert [d.model_dump() for d in devices] == [
        {"address": "AA:BB:CC:DD:EE:FF", "name": "DeviceOne", "lat": None, "lon": None},
        {
            "address": "11:22:33:44:55:66",
            "name": "Another Device",
            "lat": None,
            "lon": None,
        },
    ]
