import os
import sys
from pathlib import Path
from types import ModuleType

from piwardrive import analysis
from piwardrive.persistence import HealthRecord


def test_compute_health_stats() -> None:
    records = [
        HealthRecord("t1", 40.0, 10.0, 50.0, 20.0),
        HealthRecord("t2", 50.0, 20.0, 40.0, 30.0),
    ]
    stats = analysis.compute_health_stats(records)
    assert round(stats["temp_avg"], 1) == 45.0
    assert stats["cpu_avg"] == 15.0


def test_plot_cpu_temp_creates_file(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / "temp.png"
    records = [
        HealthRecord("2024-01-01T00:00:00", 40.0, 10.0, 50.0, 20.0),
        HealthRecord("2024-01-01T01:00:00", 50.0, 20.0, 40.0, 30.0),
    ]
    mpl = ModuleType("matplotlib")
    mpl.use = lambda *a, **k: None
    pyplot = ModuleType("matplotlib.pyplot")
    pyplot.figure = lambda *a, **k: None
    pyplot.plot = lambda *a, **k: None
    pyplot.legend = lambda *a, **k: None
    pyplot.tight_layout = lambda *a, **k: None
    pyplot.savefig = lambda p, *a, **k: open(p, "wb").close()
    pyplot.close = lambda *a, **k: None
    mpl.pyplot = pyplot
    monkeypatch.setitem(sys.modules, "matplotlib", mpl)
    monkeypatch.setitem(sys.modules, "matplotlib.pyplot", pyplot)
    analysis.plot_cpu_temp(records, str(path))
    assert path.is_file()
    path.unlink()


def test_plot_cpu_temp_plotly_backend(tmp_path: Path) -> None:
    path = tmp_path / "temp_plotly.png"
    records = [
        HealthRecord("2024-01-01T00:00:00", 40.0, 10.0, 50.0, 20.0),
        HealthRecord("2024-01-01T01:00:00", 50.0, 20.0, 40.0, 30.0),
    ]
    mpl = ModuleType("matplotlib")
    mpl.use = lambda *a, **k: None
    pyplot = ModuleType("matplotlib.pyplot")
    pyplot.figure = lambda *a, **k: None
    pyplot.plot = lambda *a, **k: None
    pyplot.legend = lambda *a, **k: None
    pyplot.tight_layout = lambda *a, **k: None
    pyplot.savefig = lambda p, *a, **k: open(p, "wb").close()
    pyplot.close = lambda *a, **k: None
    mpl.pyplot = pyplot
    sys.modules["matplotlib"] = mpl
    sys.modules["matplotlib.pyplot"] = pyplot
    analysis.plot_cpu_temp(records, str(path), backend="plotly")
    assert path.is_file()
    path.unlink()
