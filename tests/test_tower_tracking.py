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
