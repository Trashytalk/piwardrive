import importlib.util
import logging
import os

import pytest

tracker_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "src",
    "piwardrive",
    "sigint_suite",
    "cellular",
    "tower_tracker",
    "tracker.py",
)
spec = importlib.util.spec_from_file_location("tower_tracker", tracker_path)
tracker_mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(tracker_mod)
TowerTracker = tracker_mod.TowerTracker


@pytest.mark.asyncio
async def test_tracker_update_and_query(tmp_path):
    db = tmp_path / "towers.db"
    tracker = TowerTracker(str(db))
    await tracker.update_tower("id1", 1.0, 2.0, last_seen=123)
    rec = await tracker.get_tower("id1")
    assert rec is not None and rec["lat"] == 1.0
    all_rec = await tracker.all_towers()
    assert len(all_rec) == 1
    await tracker.close()


@pytest.mark.asyncio
async def test_wifi_and_bluetooth_logging(tmp_path):
    db = tmp_path / "towers.db"
    tr = TowerTracker(str(db))

    await tr.log_wifi("AA:BB:CC", "TestNet", lat=1.0, lon=2.0, timestamp=100)
    await tr.log_bluetooth("11:22:33", "Phone", lat=3.0, lon=4.0, timestamp=200)

    wifi = await tr.wifi_history("AA:BB:CC")
    bt = await tr.bluetooth_history("11:22:33")

    assert wifi and wifi[0]["ssid"] == "TestNet"
    assert bt and bt[0]["name"] == "Phone"

    await tr.close()


@pytest.mark.asyncio
async def test_async_logging_and_retrieval(tmp_path):
    db = tmp_path / "towers.db"
    tracker = TowerTracker(str(db))
    await tracker.log_wifi("DE:AD:BE", "Net", timestamp=50)
    await tracker.log_bluetooth("AA:BB:CC", "Headset", timestamp=60)
    wifi = await tracker.wifi_history("DE:AD:BE")
    bt = await tracker.bluetooth_history("AA:BB:CC")
    assert wifi and wifi[0]["timestamp"] == 50
    assert bt and bt[0]["timestamp"] == 60
    await tracker.close()


@pytest.mark.asyncio
async def test_tower_history(tmp_path):
    db = tmp_path / "towers.db"
    tr = TowerTracker(str(db))

    await tr.log_tower("tower1", "-70", lat=1.0, lon=2.0, timestamp=100)
    await tr.log_tower("tower1", "-60", lat=1.1, lon=2.1, timestamp=200)

    hist = await tr.tower_history("tower1")
    assert hist and [rec["rssi"] for rec in hist] == ["-60", "-70"]

    await tr.close()
