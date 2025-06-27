import os
import sys
from types import SimpleNamespace


def test_export_logs_script(monkeypatch, tmp_path):
    called = {}

    async def fake_export(self, path=None, lines=200):
        called["path"] = path
        called["lines"] = lines
        return "ok"

    class DummyApp:
        def __init__(self):
            pass

        export_logs = fake_export

    monkeypatch.setitem(sys.modules, "main", SimpleNamespace(PiWardriveApp=DummyApp))
    if "piwardrive.scripts.export_logs" in sys.modules:
        del sys.modules["piwardrive.scripts.export_logs"]
    import piwardrive.scripts.export_logs as ex

    ex.main([str(tmp_path / "log.txt"), "--lines", "10"])
    assert called["path"] == str(tmp_path / "log.txt")
    assert called["lines"] == 10
