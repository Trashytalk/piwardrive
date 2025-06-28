import sys
from types import ModuleType

# Minimal stubs so imports in analysis succeed
fake_aiosqlite = ModuleType("aiosqlite")
fake_aiosqlite.Connection = object  # type: ignore[attr-defined]
sys.modules.setdefault("aiosqlite", fake_aiosqlite)

fake_pydantic = ModuleType("pydantic")
fake_pydantic.BaseModel = object  # type: ignore[attr-defined]
fake_pydantic.Field = lambda *a, **k: None  # type: ignore[attr-defined]
fake_pydantic.ValidationError = type("VE", (), {})  # type: ignore[attr-defined]
fake_pydantic.field_validator = lambda *a, **k: (lambda f: f)  # type: ignore[attr-defined]
sys.modules.setdefault("pydantic", fake_pydantic)

from piwardrive import analysis  # noqa: E402


def test_compute_health_stats_empty() -> None:
    assert analysis.compute_health_stats([]) == {}
