import sys
from pathlib import Path
from types import ModuleType

from piwardrive import analysis
from piwardrive.persistence import HealthRecord


def test_plot_cpu_temp_plotly_backend(tmp_path: Path, monkeypatch) -> None:
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

    fake_go = ModuleType("plotly.graph_objects")
    fake_go.Figure = lambda: type(  # type: ignore[attr-defined]
        "F",
        (),
        {
            "add_trace": lambda *a, **k: None,
            "write_image": lambda p, *a, **k: open(p, "wb").close(),
        },
    )()
    fake_go.Scattergl = lambda *a, **k: None  # type: ignore[attr-defined]
    plotly_pkg = ModuleType("plotly")
    plotly_pkg.graph_objects = fake_go  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "plotly", plotly_pkg)
    monkeypatch.setitem(sys.modules, "plotly.graph_objects", fake_go)

    out = tmp_path / "out.png"
    rec = HealthRecord("2024-01-01T00:00:00", 40, 10, 20, 30)
    analysis.plot_cpu_temp([rec], str(out), backend="plotly")
    assert out.exists()  # nosec
