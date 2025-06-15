import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sigint_suite.cellular.imsi_catcher.scanner import scan_imsis


def test_scan_imsis_parses_output_and_tags_location(monkeypatch):
    output = "12345,310,260,-50\n67890,311,480,-60"
    monkeypatch.setattr("subprocess.check_output", lambda *a, **k: output)
    monkeypatch.setattr(
        "sigint_suite.cellular.imsi_catcher.scanner.get_position",
        lambda: (1.0, 2.0),
    )
    records = scan_imsis("dummy")
    assert records == [
        {"imsi": "12345", "mcc": "310", "mnc": "260", "rssi": "-50", "lat": 1.0, "lon": 2.0},
        {"imsi": "67890", "mcc": "311", "mnc": "480", "rssi": "-60", "lat": 1.0, "lon": 2.0},
    ]
