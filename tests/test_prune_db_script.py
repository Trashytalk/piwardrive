import sys


def test_prune_db_script(monkeypatch):
    called = {}

    async def fake_prune(days):
        called["days"] = days

    if "piwardrive.scripts.prune_db" in sys.modules:
        del sys.modules["piwardrive.scripts.prune_db"]
    import piwardrive.scripts.prune_db as pd

    monkeypatch.setattr(pd.persistence, "purge_old_health", fake_prune)
    pd.main(["30"])
    assert called.get("days") == 30
