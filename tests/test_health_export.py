import os
import sys
import json
from dataclasses import asdict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import scripts.health_export as he
from piwardrive.persistence import HealthRecord


def test_export_json(tmp_path, monkeypatch):
    rec = HealthRecord("t", 1.0, 2.0, 3.0, 4.0)

    async def fake_load(limit: int = 10):
        return [rec]

    monkeypatch.setattr(he, "load_recent_health", fake_load)
    out = tmp_path / "data.json"
    he.main([str(out), "--format", "json", "--limit", "1"])
    assert json.load(open(out)) == [asdict(rec)]


def test_export_csv(tmp_path, monkeypatch):
    rec = HealthRecord("t", 1.0, 2.0, 3.0, 4.0)

    async def fake_load(limit: int = 10):
        return [rec]

    monkeypatch.setattr(he, "load_recent_health", fake_load)
    out = tmp_path / "data.csv"
    he.main([str(out), "--format", "csv", "--limit", "1"])
    data = out.read_text()
    assert "timestamp" in data
    assert "t" in data
