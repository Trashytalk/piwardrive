import asyncio

from piwardrive.sigint_suite.cellular.tower_scanner.scanner import (
    async_scan_towers,
    scan_towers,
)


def test_scan_towers(monkeypatch):
    output = "123,-70\n456,-80"
    monkeypatch.setattr("subprocess.check_output", lambda *a, **k: output)
    monkeypatch.setattr(
        "piwardrive.sigint_suite.cellular.tower_scanner.scanner.get_position",
        lambda: None,
    )

    records = scan_towers("dummy")
    assert [r.model_dump() for r in records] == [
        {"tower_id": "123", "rssi": "-70", "lat": None, "lon": None},
        {"tower_id": "456", "rssi": "-80", "lat": None, "lon": None},
    ]


def test_async_scan_towers(monkeypatch):
    output = "123,-70"

    class DummyProc:
        async def communicate(self):
            return output.encode(), b""

    async def fake_create(*args, **kwargs):
        return DummyProc()

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_create)
    monkeypatch.setattr(asyncio, "wait_for", lambda coro, timeout: coro)
    monkeypatch.setattr(
        "piwardrive.sigint_suite.cellular.tower_scanner.scanner.get_position",
        lambda: None,
    )

    async def run():
        return await async_scan_towers("dummy")

    records = asyncio.run(run())
    assert [r.model_dump() for r in records] == [
        {"tower_id": "123", "rssi": "-70", "lat": None, "lon": None},
    ]
