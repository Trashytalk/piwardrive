import asyncio
from types import SimpleNamespace
from piwardrive.services import network_fingerprinting


class Dummy:
    def __init__(self):
        self.saved = None

    async def __call__(self, records):
        self.saved = records


def test_fingerprint_wifi_records(monkeypatch):
    dummy = Dummy()
    monkeypatch.setattr(
        network_fingerprinting.persistence,
        "save_network_fingerprints",
        dummy,
    )
    recs = [
        {
            "bssid": "AA",
            "ssid": "net",
            "vendor_oui": "AA",
            "encryption_type": "WPA2",
        }
    ]
    asyncio.run(network_fingerprinting.fingerprint_wifi_records(recs))
    assert dummy.saved and dummy.saved[0]["bssid"] == "AA"
