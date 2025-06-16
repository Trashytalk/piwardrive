import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_vacuum_script(monkeypatch):
    called = {}

    async def fake_vacuum():
        called['ok'] = True

    if 'scripts.vacuum_db' in sys.modules:
        del sys.modules['scripts.vacuum_db']
    import scripts.vacuum_db as vac
    monkeypatch.setattr(vac.persistence, 'vacuum', fake_vacuum)
    vac.main([])
    assert called.get('ok')
