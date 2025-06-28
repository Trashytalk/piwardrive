import sys
from types import SimpleNamespace


def test_export_log_bundle_script(monkeypatch, tmp_path):
    called = {}

    async def fake_bundle(self, path=None, lines=200):
        called["path"] = path
        called["lines"] = lines
        return "ok"

    class DummyApp:
        export_log_bundle = fake_bundle

    monkeypatch.setitem(sys.modules, "main", SimpleNamespace(PiWardriveApp=DummyApp))
    if "piwardrive.scripts.export_log_bundle" in sys.modules:
        del sys.modules["piwardrive.scripts.export_log_bundle"]
    import piwardrive.scripts.export_log_bundle as ex

    ex.main([str(tmp_path / "bundle.zip"), "--lines", "5"])
    assert called["path"] == str(tmp_path / "bundle.zip")
    assert called["lines"] == 5
