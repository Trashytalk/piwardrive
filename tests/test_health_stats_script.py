import json
import sys

import piwardrive.scripts.health_stats as hs
from piwardrive.persistence import HealthRecord


def test_health_stats_script_output(monkeypatch, capsys):
    records = [HealthRecord("t1", 50.0, 20.0, 30.0, 40.0)]

    async def fake_load(limit: int = 10):
        assert limit == 5
        return records

    monkeypatch.setattr(hs, "load_recent_health", fake_load)
    monkeypatch.setattr(hs, "forecast_cpu_temp", lambda r, s: [1.0] * s)
    hs.main(["--limit", "5", "--forecast", "2"])
    out_lines = [json.loads(l) for l in capsys.readouterr().out.strip().splitlines() if l]
    expected = {"temp_avg": 50.0, "cpu_avg": 20.0, "mem_avg": 30.0, "disk_avg": 40.0}
    assert out_lines[0]["message"] == json.dumps(expected)
    assert out_lines[1]["message"] == json.dumps({"forecast": [1.0, 1.0]})
