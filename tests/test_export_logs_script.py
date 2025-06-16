import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_export_logs_script(monkeypatch, tmp_path):
    called = {}

    async def fake_export(self, path=None, lines=200):
        called['path'] = path
        called['lines'] = lines
        return 'ok'

    class DummyApp:
        def __init__(self):
            pass
        export_logs = fake_export

    monkeypatch.setitem(sys.modules, 'main', SimpleNamespace(PiWardriveApp=DummyApp))
    if 'scripts.export_logs' in sys.modules:
        del sys.modules['scripts.export_logs']
    import scripts.export_logs as ex
    ex.main([str(tmp_path / 'log.txt'), '--lines', '10'])
    assert called['path'] == str(tmp_path / 'log.txt')
    assert called['lines'] == 10
