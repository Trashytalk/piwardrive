import sys
from pathlib import Path
from types import ModuleType

# Stub aiosqlite so piwardrive.persistence can import without the dependency
fake_aiosqlite = ModuleType("aiosqlite")
fake_aiosqlite.Connection = object  # type: ignore[attr-defined]
sys.modules.setdefault("aiosqlite", fake_aiosqlite)  # noqa: E402

fake_pydantic = ModuleType("pydantic")
fake_pydantic.BaseModel = object  # type: ignore[attr-defined]
fake_pydantic.Field = lambda *a, **k: None  # type: ignore[attr-defined]
fake_pydantic.ValidationError = type("VE", (), {})  # type: ignore[attr-defined]
fake_pydantic.field_validator = lambda *a, **k: (lambda f: f)  # type: ignore[attr-defined]  # noqa: E501
sys.modules.setdefault("pydantic", fake_pydantic)  # noqa: E402

from piwardrive import analysis  # noqa: E402
from piwardrive.persistence import HealthRecord  # noqa: E402


def test_compute_health_stats_empty():
    assert analysis.compute_health_stats([]) == {}  # nosec


def test_plot_cpu_temp_matplotlib_backend(tmp_path: Path, monkeypatch) -> None:
    class FakeSeries(list):
        def rolling(self, window: int, min_periods: int = 1):
            class Roll:
                def __init__(self, data: list) -> None:
                    self.data = data

                def mean(self) -> list:
                    out = []
                    for i in range(len(self.data)):
                        window_vals = [
                            t for t in self.data[max(0, i - 4) : i + 1] if t is not None
                        ]
                        out.append(
                            sum(window_vals) / len(window_vals)
                            if window_vals
                            else float("nan")
                        )
                    return out

            return Roll(self)

    class FakeDataFrame(dict):
        def __init__(self, rows: list) -> None:
            self.update({k: [r[k] for r in rows] for k in rows[0]})

        def __getitem__(self, key: str):
            val = super().__getitem__(key)
            if isinstance(val, list):
                return FakeSeries(val)
            return val

        def __setitem__(self, key: str, value: list) -> None:
            super().__setitem__(key, list(value))

        def sort_values(self, col: str, inplace: bool = True) -> None:
            order = sorted(range(len(self[col])), key=lambda i: self[col][i])
            for k, v in self.items():
                if isinstance(v, list):
                    self[k] = [v[i] for i in order]

    fake_pd = ModuleType("pandas")
    fake_pd.DataFrame = FakeDataFrame  # type: ignore[attr-defined]
    fake_pd.to_datetime = lambda x: x  # type: ignore[attr-defined]
    monkeypatch.setattr(analysis, "pd", fake_pd)

    mpl = ModuleType("matplotlib")
    mpl.use = lambda *a, **k: None  # type: ignore[attr-defined]
    pyplot = ModuleType("matplotlib.pyplot")
    pyplot.figure = lambda *a, **k: None  # type: ignore[attr-defined]
    pyplot.plot = lambda *a, **k: None  # type: ignore[attr-defined]
    pyplot.legend = lambda *a, **k: None  # type: ignore[attr-defined]
    pyplot.tight_layout = lambda *a, **k: None  # type: ignore[attr-defined]
    pyplot.savefig = lambda p, *a, **k: open(p, "wb").close()  # type: ignore[attr-defined]  # noqa: E501
    pyplot.close = lambda *a, **k: None  # type: ignore[attr-defined]
    mpl.pyplot = pyplot  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "matplotlib", mpl)
    monkeypatch.setitem(sys.modules, "matplotlib.pyplot", pyplot)

    out = tmp_path / "out.png"
    rec = HealthRecord("2024-01-01T00:00:00", 40, 10, 20, 30)
    analysis.plot_cpu_temp([rec], str(out), backend="matplotlib")
    assert out.exists()  # nosec


def test_plot_cpu_temp_no_pandas(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(analysis, "pd", None)
    mpl = ModuleType("matplotlib")
    mpl.use = lambda *a, **k: None  # type: ignore[attr-defined]
    pyplot = ModuleType("matplotlib.pyplot")
    pyplot.figure = lambda *a, **k: None  # type: ignore[attr-defined]
    pyplot.plot = lambda *a, **k: None  # type: ignore[attr-defined]
    pyplot.legend = lambda *a, **k: None  # type: ignore[attr-defined]
    pyplot.tight_layout = lambda *a, **k: None  # type: ignore[attr-defined]
    pyplot.savefig = lambda p, *a, **k: open(p, "wb").close()  # type: ignore[attr-defined]  # noqa: E501
    pyplot.close = lambda *a, **k: None  # type: ignore[attr-defined]
    mpl.pyplot = pyplot  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "matplotlib", mpl)
    monkeypatch.setitem(sys.modules, "matplotlib.pyplot", pyplot)
    out = tmp_path / "out.png"
    rec = HealthRecord("2024-01-01T00:00:00", 40, 10, 20, 30)
    analysis.plot_cpu_temp([rec], str(out))
    assert out.exists()  # nosec


def test_plot_cpu_temp_plotly(tmp_path: Path, monkeypatch):
    class FakeSeries(list):
        def rolling(self, window, min_periods=1):
            class Roll:
                def __init__(self, data):
                    self.data = data

                def mean(self):
                    out = []
                    for i in range(len(self.data)):
                        window_vals = [
                            t for t in self.data[max(0, i - 4) : i + 1] if t is not None
                        ]
                        out.append(
                            sum(window_vals) / len(window_vals)
                            if window_vals
                            else float("nan")
                        )
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
    fake_pd.DataFrame = FakeDataFrame  # type: ignore[attr-defined]
    fake_pd.to_datetime = lambda x: x  # type: ignore[attr-defined]
    monkeypatch.setattr(analysis, "pd", fake_pd)

    fake = ModuleType("plotly.graph_objects")
    fake.Figure = lambda: type(  # type: ignore[attr-defined]
        "F",
        (),
        {
            "add_trace": lambda *a, **k: None,
            "write_image": lambda *a, **k: open(tmp_path / "out.png", "wb").close(),
        },
    )()
    fake.Scattergl = lambda *a, **k: None  # type: ignore[attr-defined]
    plotly_pkg = ModuleType("plotly")
    plotly_pkg.graph_objects = fake  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "plotly", plotly_pkg)
    monkeypatch.setitem(sys.modules, "plotly.graph_objects", fake)

    out = tmp_path / "out.png"
    rec = HealthRecord("2024-01-01T00:00:00", 40, 10, 20, 30)
    analysis.plot_cpu_temp([rec], str(out), backend="plotly")
    assert out.exists()  # nosec
