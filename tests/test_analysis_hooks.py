import sys
from types import ModuleType

# Stub aiosqlite so importing persistence works without the dependency
fake_aiosqlite = ModuleType("aiosqlite")
fake_aiosqlite.Connection = object  # type: ignore[attr-defined]
sys.modules.setdefault("aiosqlite", fake_aiosqlite)

# Minimal pydantic stub for config import
fake_pydantic = ModuleType("pydantic")
fake_pydantic.BaseModel = object  # type: ignore[attr-defined]
fake_pydantic.Field = lambda *a, **k: None  # type: ignore[attr-defined]
fake_pydantic.ValidationError = type("VE", (), {})  # type: ignore[attr-defined]
fake_pydantic.field_validator = lambda *a,
    **k: (lambda f: f)  # type: ignore[attr-defined]
sys.modules.setdefault("pydantic", fake_pydantic)

from piwardrive import analysis
from piwardrive.persistence import HealthRecord


def test_ml_hook_invoked():
    called = []

    def hook(rec: HealthRecord) -> None:
        called.append(rec.timestamp)

    analysis.register_ml_hook(hook)
    rec = HealthRecord("t", 1.0, 2.0, 3.0, 4.0)
    analysis.process_new_record(rec)
    assert called == ["t"]
