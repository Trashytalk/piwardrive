import os
import sys
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sigint_suite.cellular.band_scanner.scanner import scan_bands


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
