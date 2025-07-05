import sys
from types import SimpleNamespace


def test_vacuum_script(monkeypatch):
    called = {}

    async def fake_vacuum():
        called["ok"] = True

    if "piwardrive.scripts.vacuum_db" in sys.modules:
        del sys.modules["piwardrive.scripts.vacuum_db"]
    import piwardrive.scripts.vacuum_db as vac

    monkeypatch.setattr(vac.persistence, "vacuum", fake_vacuum)
    vac.main([])
    assert called.get("ok")
