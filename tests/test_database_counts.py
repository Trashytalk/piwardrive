import asyncio
import os
import sys
from types import SimpleNamespace

import pytest


@pytest.fixture(autouse=True)
def _stub_pydantic(monkeypatch):
    module = SimpleNamespace(
        BaseModel=object,
        Field=lambda *a, **k: None,
        ValidationError=Exception,
        field_validator=lambda *a, **k: (lambda f: f),
    )
    monkeypatch.setitem(sys.modules, "pydantic", module)


def setup_tmp(tmp_path):
    from piwardrive import config

    config.CONFIG_DIR = str(tmp_path)
    os.environ["PW_DB_PATH"] = str(tmp_path / "app.db")


def test_get_table_counts(tmp_path):
    import pytest

    pytest.importorskip("aiosqlite")
    from piwardrive.core import persistence

    setup_tmp(tmp_path)
    rec = persistence.HealthRecord("t", 1.0, 1.0, 1.0, 1.0)
    asyncio.run(persistence.save_health_record(rec))
    asyncio.run(persistence.flush_health_records())
    counts = asyncio.run(persistence.get_table_counts())
    assert counts.get("health_records") == 1  # nosec B101
