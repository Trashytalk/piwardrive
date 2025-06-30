import asyncio
import json

import piwardrive.sigint_suite.continuous_scan as cs
import piwardrive.sigint_suite.scripts.continuous_scan as cli


def test_scan_once_returns_data(monkeypatch):
    monkeypatch.setattr(cs, "scan_wifi", lambda: [{"ssid": "x"}])
    monkeypatch.setattr(cs, "scan_bluetooth", lambda: [{"address": "a"}])
    result = cs.scan_once()
    assert result["wifi"][0]["ssid"] == "x"
    assert result["bluetooth"][0]["address"] == "a"


def test_run_continuous_scan_iterations(monkeypatch):
    calls = {"n": 0}

    async def fake_wifi():
        return []

    async def fake_bt():
        return []

    monkeypatch.setattr(cs, "async_scan_wifi", fake_wifi)
    monkeypatch.setattr(cs, "async_scan_bluetooth", fake_bt)

    orig_sleep = asyncio.sleep

    async def fast_sleep(_):
        await orig_sleep(0)

    monkeypatch.setattr(cs.asyncio, "sleep", fast_sleep)

    asyncio.run(
        cs.run_continuous_scan(
            interval=0,
            iterations=3,
            on_result=lambda _r: calls.update(n=calls["n"] + 1),
        )
    )
    assert calls["n"] == 3


def test_run_once_writes_json(tmp_path, monkeypatch):
    monkeypatch.setattr(
        cs,
        "scan_once",
        lambda: {"wifi": [{"ssid": "x"}], "bluetooth": [{"address": "a"}]},
    )
    cli.run_once(str(tmp_path))
    wifi = json.load(open(tmp_path / "wifi.json"))
    bt = json.load(open(tmp_path / "bluetooth.json"))
    assert wifi[0]["ssid"] == "x"
    assert bt[0]["address"] == "a"


def test_main_runs_iterations(tmp_path, monkeypatch):
    calls = {"n": 0}

    def fake_save(_dir: str, _res: cs.Result) -> None:
        calls["n"] += 1

    monkeypatch.setattr(cli, "_save_results", fake_save)

    async def fake_wifi():
        return []

    async def fake_bt():
        return []

    monkeypatch.setattr(cs, "async_scan_wifi", fake_wifi)
    monkeypatch.setattr(cs, "async_scan_bluetooth", fake_bt)

    orig_sleep = asyncio.sleep

    async def fast_sleep(_):
        await orig_sleep(0)

    monkeypatch.setattr(cs.asyncio, "sleep", fast_sleep)

    cli.main(["--interval", "0", "--iterations", "3", "--export-dir", str(tmp_path)])
    assert calls["n"] == 3
