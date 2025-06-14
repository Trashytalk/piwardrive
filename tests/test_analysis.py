import os
import sys
from types import ModuleType
from pathlib import Path

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


def test_plot_cpu_temp_creates_file(tmp_path: Path) -> None:
    path = tmp_path / "temp.png"
    records = [
        HealthRecord("2024-01-01T00:00:00", 40.0, 10.0, 50.0, 20.0),
        HealthRecord("2024-01-01T01:00:00", 50.0, 20.0, 40.0, 30.0),
    ]
    analysis.plot_cpu_temp(records, str(path))
    assert path.is_file()
    path.unlink()
