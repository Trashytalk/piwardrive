import asyncio
import os
import sys
import types

from piwardrive.sigint_suite.cellular.band_scanner.scanner import (
    async_scan_bands, scan_bands)


def test_scan_bands_parses_output(monkeypatch):
    output = "LTE,100,-60\n5G,200,-70"
    monkeypatch.setattr("subprocess.check_output", lambda *a, **k: output)
    records = scan_bands("dummy")
    assert [r.model_dump() for r in records] == [
        {"band": "LTE", "channel": "100", "rssi": "-60"},
        {"band": "5G", "channel": "200", "rssi": "-70"},
    ]


def test_scan_bands_passes_timeout(monkeypatch):
    called = {}

    def fake_check_output(*a, **k):
        called["timeout"] = k.get("timeout")
        return ""

    monkeypatch.setattr("subprocess.check_output", fake_check_output)

    scan_bands("dummy", timeout=5)

    assert called["timeout"] == 5


def test_async_scan_bands(monkeypatch):
    output = "LTE,100,-60\n5G,200,-70"

    class DummyProc:
        async def communicate(self):
            return output.encode(), b""

    async def fake_create(*args, **kwargs):
        return DummyProc()

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_create)
    monkeypatch.setattr(asyncio, "wait_for", lambda coro, timeout: coro)

    async def run():
        return await async_scan_bands("dummy")

    records = asyncio.run(run())
    assert [r.model_dump() for r in records] == [
        {"band": "LTE", "channel": "100", "rssi": "-60"},
        {"band": "5G", "channel": "200", "rssi": "-70"},
    ]
