import sys
from types import ModuleType
from pathlib import Path

from piwardrive import analysis
from piwardrive.persistence import HealthRecord


def test_compute_health_stats_empty():
    assert analysis.compute_health_stats([]) == {}


def test_plot_cpu_temp_no_pandas(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(analysis, "pd", None)
    mpl = ModuleType("matplotlib")
    mpl.use = lambda *a, **k: None
    pyplot = ModuleType("matplotlib.pyplot")
    pyplot.figure = pyplot.plot = pyplot.legend = \
        pyplot.tight_layout = lambda *a, **k: None
    pyplot.savefig = lambda p, *a, **k: open(p, "wb").close()
    pyplot.close = lambda *a, **k: None
    mpl.pyplot = pyplot
    monkeypatch.setitem(sys.modules, "matplotlib", mpl)
    monkeypatch.setitem(sys.modules, "matplotlib.pyplot", pyplot)
    out = tmp_path / "out.png"
    rec = HealthRecord("2024-01-01T00:00:00", 40, 10, 20, 30)
    analysis.plot_cpu_temp([rec], str(out))
    assert out.exists()


def test_plot_cpu_temp_plotly(tmp_path: Path, monkeypatch):
    class FakeSeries(list):
        def rolling(self, window, min_periods=1):
            class Roll:
                def __init__(self, data):
                    self.data = data

                def mean(self):
                    out = []
                    for i in range(len(self.data)):
                        window_vals = [t for t in self.data[max(0, i - 4) : i + 1] if t is not None]
                        out.append(sum(window_vals) / len(window_vals) if window_vals else float("nan"))
                    return out

            return Roll(self)

    class FakeDataFrame(dict):
        def __init__(self, rows):
            self.update({k: [r[k] for r in rows] for k in rows[0]})

        def __getitem__(self, key):
            val = super().__getitem__(key)
            if isinstance(val, list):
                return FakeSeries(val)
            return val

        def __setitem__(self, key, value):
            super().__setitem__(key, list(value))

        def sort_values(self, col, inplace=True):
            order = sorted(range(len(self[col])), key=lambda i: self[col][i])
            for k, v in self.items():
                if isinstance(v, list):
                    self[k] = [v[i] for i in order]

    fake_pd = ModuleType("pandas")
    fake_pd.DataFrame = FakeDataFrame
    fake_pd.to_datetime = lambda x: x
    monkeypatch.setattr(analysis, "pd", fake_pd)

    fake = ModuleType("plotly.graph_objects")
    fake.Figure = lambda: type(
        "F",
        (),
        {
            "add_trace": lambda *a, **k: None,
            "write_image": lambda *a, **k: open(tmp_path / "out.png", "wb").close(),
        },
    )()
    fake.Scattergl = lambda *a, **k: None
    plotly_pkg = ModuleType("plotly")
    plotly_pkg.graph_objects = fake
    monkeypatch.setitem(sys.modules, "plotly", plotly_pkg)
    monkeypatch.setitem(sys.modules, "plotly.graph_objects", fake)

    out = tmp_path / "out.png"
    rec = HealthRecord("2024-01-01T00:00:00", 40, 10, 20, 30)
    analysis.plot_cpu_temp([rec], str(out), backend="plotly")
    assert out.exists()
