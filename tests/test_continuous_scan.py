import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import piwardrive.sigint_suite.scripts.continuous_scan as cs


def test_run_once_writes_json(tmp_path, monkeypatch):
    monkeypatch.setattr(cs, "scan_wifi", lambda: [{"ssid": "x"}])
    monkeypatch.setattr(cs, "scan_bluetooth", lambda: [{"address": "a"}])
    cs.run_once(str(tmp_path))
    wifi = json.load(open(tmp_path / "wifi.json"))
    bt = json.load(open(tmp_path / "bluetooth.json"))
    assert wifi[0]["ssid"] == "x"
    assert bt[0]["address"] == "a"


def test_main_runs_iterations(tmp_path, monkeypatch):
    calls = {"n": 0}

    def fake_run_once(_dir: str) -> None:
        calls["n"] += 1

    monkeypatch.setattr(cs, "run_once", fake_run_once)
    monkeypatch.setattr(cs.time, "sleep", lambda _s: None)
    cs.main(["--interval", "0", "--iterations", "3", "--export-dir", str(tmp_path)])
    assert calls["n"] == 3
