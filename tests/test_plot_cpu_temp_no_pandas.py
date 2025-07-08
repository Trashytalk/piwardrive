import sys
from pathlib import Path
from types import ModuleType

# Stub aiosqlite and pydantic so piwardrive imports succeed
fake_aiosqlite = ModuleType("aiosqlite")fake_aiosqlite.Connection = object  # type: ignore[attr-defined]sys.modules.setdefault("aiosqlite", fake_aiosqlite)fake_pydantic = ModuleType("pydantic")
fake_pydantic.BaseModel = object  # type: ignore[attr-defined]fake_pydantic.Field = lambda *a, **k: None  # type: ignore[attr-defined]fake_pydantic.ValidationError = type("VE", (), {})  # type: ignore[attr-defined]fake_pydantic.field_validator = lambda *a,**k: (lambda f: f)  # type: ignore[attr-defined]sys.modules.setdefault("pydantic", fake_pydantic)

from piwardrive import analysis
from piwardrive.persistence import HealthRecord

def test_plot_cpu_temp_no_pandas_simple(tmp_path: Path, monkeypatch) -> None:monkeypatch.setattr(analysis, "pd", None)mpl = ModuleType("matplotlib")mpl.use = lambda *a, **k: None  # type: ignore[attr-defined]pyplot = ModuleType("matplotlib.pyplot")
    pyplot.figure = lambda *a, **k: None  # type: ignore[attr-defined]
    pyplot.plot = lambda *a, **k: None  # type: ignore[attr-defined]
    pyplot.legend = lambda *a, **k: None  # type: ignore[attr-defined]
    pyplot.tight_layout = lambda *a, **k: None  # type: ignore[attr-defined]pyplot.savefig = lambda p,*a,**k: open(p,"wb").close()  # type: ignore[attr-defined]
    pyplot.close = lambda *a, **k: None  # type: ignore[attr-defined]mpl.pyplot = pyplot  # type: ignore[attr-defined]monkeypatch.setitem(sys.modules, "matplotlib", mpl)
    monkeypatch.setitem(sys.modules, "matplotlib.pyplot", pyplot)out = tmp_path / "out.png"
    rec = HealthRecord("2024-01-01T00:00:00", 40.0, 10.0, 20.0, 30.0)
    analysis.plot_cpu_temp([rec], str(out))
    assert out.exists()
