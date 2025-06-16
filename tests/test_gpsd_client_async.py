import os
import sys
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import gpsd_client_async


def test_async_methods_return_values(monkeypatch):
    async def direct(func, *args, **kwargs):
        return func(*args, **kwargs)

    monkeypatch.setattr(gpsd_client_async.asyncio, "to_thread", direct)
    monkeypatch.setattr(gpsd_client_async.GPSDClient, "get_position", lambda self: (1.0, 2.0))
    monkeypatch.setattr(gpsd_client_async.GPSDClient, "get_accuracy", lambda self: 3.0)
    monkeypatch.setattr(gpsd_client_async.GPSDClient, "get_fix_quality", lambda self: "3D")

    client = gpsd_client_async.AsyncGPSDClient()

    assert asyncio.run(client.get_position_async()) == (1.0, 2.0)
    assert asyncio.run(client.get_accuracy_async()) == 3.0
    assert asyncio.run(client.get_fix_quality_async()) == "3D"

def test_async_methods_failures(monkeypatch):
    async def direct(func, *args, **kwargs):
        return func(*args, **kwargs)

    monkeypatch.setattr(gpsd_client_async.asyncio, "to_thread", direct)
    monkeypatch.setattr(gpsd_client_async.GPSDClient, "get_position", lambda self: None)
    monkeypatch.setattr(gpsd_client_async.GPSDClient, "get_accuracy", lambda self: None)
    monkeypatch.setattr(gpsd_client_async.GPSDClient, "get_fix_quality", lambda self: "Unknown")

    client = gpsd_client_async.AsyncGPSDClient()

    assert asyncio.run(client.get_position_async()) is None
    assert asyncio.run(client.get_accuracy_async()) is None
    assert asyncio.run(client.get_fix_quality_async()) == "Unknown"
