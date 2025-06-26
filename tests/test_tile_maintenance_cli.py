import os
import sys
from types import SimpleNamespace
import pytest


@pytest.fixture(autouse=True)
def _dummy_modules(monkeypatch):
    modules = {
        "piwardrive.sigint_suite.models": SimpleNamespace(BluetoothDevice=object),
        "psutil": SimpleNamespace(net_io_counters=lambda: SimpleNamespace()),
        "aiohttp": SimpleNamespace(),
    }
    for name, mod in modules.items():
        monkeypatch.setitem(sys.modules, name, mod)
    yield


from types import ModuleType

modules = {
    "piwardrive.sigint_suite.models": SimpleNamespace(BluetoothDevice=object),
    "psutil": SimpleNamespace(net_io_counters=lambda: SimpleNamespace()),
    "aiohttp": SimpleNamespace(),
}
for name, mod in modules.items():
    module = ModuleType(name)
    module.__dict__.update(mod.__dict__)
    sys.modules[name] = module


def test_tile_maintenance_cli(monkeypatch):
    called = {}

    def fake_purge(folder, days):
        called["purge"] = (folder, days)

    def fake_limit(folder, limit):
        called["limit"] = (folder, limit)

    def fake_vacuum(path):
        called["vacuum"] = path

    if "piwardrive.scripts.tile_maintenance_cli" in sys.modules:
        del sys.modules["piwardrive.scripts.tile_maintenance_cli"]
    import piwardrive.scripts.tile_maintenance_cli as cli

    monkeypatch.setattr(cli.tile_maintenance, "purge_old_tiles", fake_purge)
    monkeypatch.setattr(cli.tile_maintenance, "enforce_cache_limit", fake_limit)
    monkeypatch.setattr(cli.tile_maintenance, "vacuum_mbtiles", fake_vacuum)

    cli.main([
        "--purge",
        "--limit",
        "--vacuum",
        "--offline",
        "db.mbtiles",
        "--folder",
        "cache",
        "--max-age-days",
        "1",
        "--limit-mb",
        "2",
    ])

    assert called["purge"] == ("cache", 1)
    assert called["limit"] == ("cache", 2)
    assert called["vacuum"] == "db.mbtiles"
