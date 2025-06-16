import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sigint_suite.cellular.tower_tracker import TowerTracker


def test_tracker_update_and_query(tmp_path):
    db = tmp_path / "towers.db"
    tracker = TowerTracker(str(db))
    tracker.update_tower("id1", 1.0, 2.0, last_seen=123)
    rec = tracker.get_tower("id1")
    assert rec is not None and rec["lat"] == 1.0
    all_rec = tracker.all_towers()
    assert len(all_rec) == 1
    tracker.close()


def test_wifi_and_bluetooth_logging(tmp_path):
    db = tmp_path / "towers.db"
    tr = TowerTracker(str(db))

    tr.log_wifi("AA:BB:CC", "TestNet", lat=1.0, lon=2.0, timestamp=100)
    tr.log_bluetooth("11:22:33", "Phone", lat=3.0, lon=4.0, timestamp=200)

    wifi = tr.wifi_history("AA:BB:CC")
    bt = tr.bluetooth_history("11:22:33")

    assert wifi and wifi[0]["ssid"] == "TestNet"
    assert bt and bt[0]["name"] == "Phone"

    tr.close()
