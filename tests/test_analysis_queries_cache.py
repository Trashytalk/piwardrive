import asyncio
import sys
from types import ModuleType

sys.modules.setdefault("psutil", ModuleType("psutil"))

from piwardrive.services import analysis_queries


class CallCounter:
    def __init__(self):
        self.count = 0
    async def __call__(self, *a, **k):
        self.count += 1
        return [{"data": 1}]


def test_cached_fetch(monkeypatch):
    counter = CallCounter()
    monkeypatch.setattr(analysis_queries.db_service, "fetch", counter)
    asyncio.run(analysis_queries.clear_cache())
    first = asyncio.run(analysis_queries.evil_twin_detection())
    second = asyncio.run(analysis_queries.evil_twin_detection())
    assert first == second == [{"data": 1}]
    assert counter.count == 1

