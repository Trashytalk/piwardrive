import sys
import asyncio
from types import ModuleType, SimpleNamespace


aiohttp_mod = ModuleType('aiohttp')
aiohttp_mod.ClientSession = object  # type: ignore[attr-defined]
aiohttp_mod.ClientTimeout = lambda *a, **k: None  # type: ignore[attr-defined]
aiohttp_mod.ClientError = Exception  # type: ignore[attr-defined]
sys.modules['aiohttp'] = aiohttp_mod

from piwardrive import sync

class DummyConfig(SimpleNamespace):
    remote_sync_url: str = 'http://remote'
    remote_sync_token: str = ''
    remote_sync_timeout: int = 5
    remote_sync_retries: int = 2


def test_upload_data_retries(monkeypatch):
    calls = []

    class Resp:
        status = 200
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass

    class Session:
        def __init__(self):
            self.calls = 0
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass
        def post(self, url, data=None, headers=None):
            calls.append(url)
            if len(calls) == 1:
                raise sync.aiohttp.ClientError('fail')
            return Resp()

    monkeypatch.setattr(sync.aiohttp, 'ClientSession', lambda *a, **k: Session())
    monkeypatch.setattr(sync, 'config', SimpleNamespace(AppConfig=SimpleNamespace(load=lambda: DummyConfig())))
    async def _noop(*_a, **_k):
        return None
    monkeypatch.setattr(sync.asyncio, 'sleep', _noop)

    fut = sync.upload_data([{'a': 1}])
    result = asyncio.run(fut)
    assert result is True
    assert calls == ['http://remote', 'http://remote']


def test_upload_data_failure(monkeypatch):
    class Resp:
        status = 500
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass

    class Session:
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass
        def post(self, url, data=None, headers=None):
            return Resp()

    monkeypatch.setattr(sync.aiohttp, 'ClientSession', lambda *a, **k: Session())
    monkeypatch.setattr(sync, 'config', SimpleNamespace(AppConfig=SimpleNamespace(load=lambda: DummyConfig())))
    async def _noop(*_a, **_k):
        return None
    monkeypatch.setattr(sync.asyncio, 'sleep', _noop)

    fut = sync.upload_data([{'a': 1}])
    result = asyncio.run(fut)
    assert result is False

