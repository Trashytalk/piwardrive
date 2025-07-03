import asyncio

from piwardrive.gpsd_client_async import AsyncGPSDClient


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def test_get_position_async(monkeypatch):
    client = AsyncGPSDClient()

    async def fake_poll():
        return {"lat": 1.0, "lon": 2.0}

    monkeypatch.setattr(client, "_poll", fake_poll)
    assert run(client.get_position_async()) == (1.0, 2.0)  # nosec B101


def test_get_accuracy_async(monkeypatch):
    client = AsyncGPSDClient()

    async def fake_poll():
        return {"epx": 3.0, "epy": 4.0}

    monkeypatch.setattr(client, "_poll", fake_poll)
    assert run(client.get_accuracy_async()) == 4.0  # nosec B101


def test_get_fix_quality_async(monkeypatch):
    client = AsyncGPSDClient()

    async def fake_poll():
        return {"mode": 2}

    monkeypatch.setattr(client, "_poll", fake_poll)
    assert run(client.get_fix_quality_async()) == "2D"  # nosec B101


def test_async_methods_none(monkeypatch):
    client = AsyncGPSDClient()

    async def fake_poll():
        return None

    monkeypatch.setattr(client, "_poll", fake_poll)
    assert run(client.get_position_async()) is None  # nosec B101
    assert run(client.get_accuracy_async()) is None  # nosec B101
    assert run(client.get_fix_quality_async()) == "Unknown"  # nosec B101
