import asyncio
from datetime import datetime, timedelta

from piwardrive import analytics
from piwardrive.persistence import HealthRecord


def test_analyze_health_baseline() -> None:
    recent = [HealthRecord("t1", 40.0, 20.0, 30.0, 40.0)]
    base = [HealthRecord("t0", 30.0, 10.0, 20.0, 30.0)]
    result = analytics.analyze_health_baseline(recent, base, threshold=5.0)
    assert result["delta"]["cpu_avg"] == 10.0
    assert "cpu_avg" in result["anomalies"]


def test_load_baseline_health(tmp_path) -> None:
    from piwardrive import config, persistence

    config.CONFIG_DIR = str(tmp_path)
    now = datetime.now()
    old_rec = HealthRecord((now - timedelta(days=40)).isoformat(), 1, 1, 1, 1)
    new_rec = HealthRecord((now - timedelta(days=5)).isoformat(), 2, 2, 2, 2)
    asyncio.run(persistence.save_health_record(old_rec))
    asyncio.run(persistence.save_health_record(new_rec))
    rows = asyncio.run(analytics.load_baseline_health(30, 10))
    assert len(rows) == 1
    assert rows[0].timestamp == old_rec.timestamp
