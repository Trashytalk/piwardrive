import asyncio

from piwardrive import wigle_integration as wi


class FakeResp:
    def __init__(self, data):
        self._data = data

    async def json(self):
        return self._data

    def raise_for_status(self):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass


class FakeSession:
    def __init__(self, data):
        self._data = data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    def get(self, *_a, **_k):
        return FakeResp(self._data)


def test_fetch_wigle_networks(monkeypatch, add_dummy_module):
    add_dummy_module("persistence")
    add_dummy_module("utils")
    data = {
        "results": [
            {
                "netid": "AA:BB:CC",
                "ssid": "Net",
                "encryption": "WPA2",
                "trilat": 1.0,
                "trilong": 2.0,
            }
        ]
    }

    monkeypatch.setattr(wi.aiohttp, "ClientSession", lambda *a, **k: FakeSession(data))

    nets = asyncio.run(wi.fetch_wigle_networks("u", "k", 1.0, 2.0))

    assert nets == [
        {"bssid": "AA:BB:CC", "ssid": "Net", "encryption": "WPA2", "lat": 1.0, "lon": 2.0}
    ]


def test_fetch_wigle_networks_cache(monkeypatch, add_dummy_module):
    add_dummy_module("persistence")
    add_dummy_module("utils")
    calls: list[int] = []
    data = {"results": []}

    class Session(FakeSession):
        def get(self, *_a, **_k):
            calls.append(1)
            return super().get(*_a, **_k)

    monkeypatch.setattr(wi.aiohttp, "ClientSession", lambda *a, **k: Session(data))
    times = [0.0, 1.0, 40.0]
    import piwardrive.core.utils as cu

    monkeypatch.setattr(cu.time, "time", lambda: times.pop(0))

    asyncio.run(wi.fetch_wigle_networks("u", "k", 1.0, 2.0))
    asyncio.run(wi.fetch_wigle_networks("u", "k", 1.0, 2.0))
    assert len(calls) == 1
    asyncio.run(wi.fetch_wigle_networks("u", "k", 1.0, 2.0))
    assert len(calls) == 2
