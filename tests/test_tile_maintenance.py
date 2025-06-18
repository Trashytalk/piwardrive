import os
import sys
import time
from types import SimpleNamespace
from pathlib import Path


modules = {
    "piwardrive.sigint_suite.models": SimpleNamespace(BluetoothDevice=object),
    "psutil": SimpleNamespace(net_io_counters=lambda: SimpleNamespace()),
    "aiohttp": SimpleNamespace(),
}
for name, mod in modules.items():
    sys.modules[name] = mod
sys.modules.setdefault("requests", SimpleNamespace(RequestException=Exception))
sys.modules.setdefault(
    "aiosqlite",
    SimpleNamespace(Connection=object, Row=object, connect=lambda p: None),
)
sys.modules.setdefault("pydantic", SimpleNamespace(BaseModel=object, Field=lambda *a, **k: None, ValidationError=Exception, field_validator=lambda *a, **k: lambda x: x))

from piwardrive import tile_maintenance  # noqa: E402
from piwardrive.scheduler import PollScheduler  # noqa: E402


class DummyScheduler:
    def __init__(self) -> None:
        self.scheduled: list[tuple[str, int]] = []

    def schedule(self, name: str, cb: any, interval: int) -> None:
        self.scheduled.append((name, interval))
        cb(0)

    def cancel(self, name: str) -> None:
        pass


def test_tile_maintenance_runs(tmp_path: Path, monkeypatch):
    folder = tmp_path / "tiles"
    folder.mkdir()
    old = folder / "old.png"
    old.write_text("x")
    recent = folder / "new.png"
    recent.write_text("y")
    os.utime(old, (time.time() - 90000, time.time() - 90000))

    called = {}

    class DummyConn:
        def __init__(self, path):
            called["path"] = path
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass
        def execute(self, sql):
            called["sql"] = sql

    monkeypatch.setattr(tile_maintenance.sqlite3, "connect", lambda p: DummyConn(p))

    sched = DummyScheduler()
    (tmp_path / "off.mbtiles").write_text("db")
    maint = tile_maintenance.TileMaintainer(
        sched,
        folder=str(folder),
        offline_path=str(tmp_path / "off.mbtiles"),
        interval=0,
        max_age_days=1,
        limit_mb=1,
        vacuum=True,
        trigger_file_count=1,
        start_observer=False,
    )
    maint.check_thresholds()
    time.sleep(0.05)
    assert not sched.scheduled
    assert not old.exists()
    assert recent.exists()
    assert called.get("sql") == "VACUUM"

