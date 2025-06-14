import os
import sys
from types import ModuleType

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import analysis
from persistence import HealthRecord


def test_compute_health_stats() -> None:
    records = [
        HealthRecord("t1", 40.0, 10.0, 50.0, 20.0),
        HealthRecord("t2", 50.0, 20.0, 40.0, 30.0),
    ]
    stats = analysis.compute_health_stats(records)
    assert round(stats["temp_avg"], 1) == 45.0
    assert stats["cpu_avg"] == 15.0
