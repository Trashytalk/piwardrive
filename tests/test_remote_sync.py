import sys
import asyncio
import io
from types import ModuleType
import pytest


# stub aiohttp before importing module
aiohttp_mod = ModuleType('aiohttp')
aiohttp_mod.ClientSession = object
aiohttp_mod.ClientTimeout = lambda *a, **k: None
aiohttp_mod.ClientError = Exception
aiohttp_mod.FormData = lambda: type('FormData', (), {'add_field': lambda *a, **k: None})()
sys.modules['aiohttp'] = aiohttp_mod

from piwardrive import remote_sync


def test_sync_database_retries(monkeypatch):
    calls = []
    sleeps = []

    class Resp:
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass
        def raise_for_status(self):
            pass

    class Session:
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass
        def post(self, url, data=None):
            calls.append(url)
            if len(calls) == 1:
                raise remote_sync.aiohttp.ClientError('fail')
            return Resp()

    monkeypatch.setattr(remote_sync.aiohttp, 'ClientSession', lambda *a, **k: Session())
    monkeypatch.setattr(remote_sync.aiohttp, 'ClientTimeout', lambda *a, **k: None)
    monkeypatch.setattr(remote_sync.os.path, 'exists', lambda _p: True)
    monkeypatch.setattr('builtins.open', lambda *_a, **_k: io.BytesIO(b'x'))

    async def fake_sleep(d):
        sleeps.append(d)
    monkeypatch.setattr(remote_sync.asyncio, 'sleep', fake_sleep)

    asyncio.run(remote_sync.sync_database_to_server('db', 'http://remote', retries=2))
    assert calls == ['http://remote', 'http://remote']
    assert sleeps == [1.0]


def test_sync_database_failure(monkeypatch):
    class Session:
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass
        def post(self, url, data=None):
            raise remote_sync.aiohttp.ClientError('fail')

    monkeypatch.setattr(remote_sync.aiohttp, 'ClientSession', lambda *a, **k: Session())
    monkeypatch.setattr(remote_sync.aiohttp, 'ClientTimeout', lambda *a, **k: None)
    monkeypatch.setattr(remote_sync.os.path, 'exists', lambda _p: True)
    monkeypatch.setattr('builtins.open', lambda *_a, **_k: io.BytesIO(b'x'))

    async def fake_sleep(_):
        pass
    monkeypatch.setattr(remote_sync.asyncio, 'sleep', fake_sleep)

    with pytest.raises(remote_sync.aiohttp.ClientError):
        asyncio.run(remote_sync.sync_database_to_server('db', 'http://remote', retries=2))
