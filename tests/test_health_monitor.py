import sys
import os
from unittest import mock
from typing import Any, cast
from types import ModuleType

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
aiohttp_mod = ModuleType('aiohttp')
aiohttp_mod.ClientSession = object
aiohttp_mod.ClientTimeout = lambda *a, **k: None
aiohttp_mod.ClientError = Exception
sys.modules['aiohttp'] = aiohttp_mod
import diagnostics
from scheduler import PollScheduler


class DummyScheduler:
    def __init__(self) -> None:
        self.scheduled: list[tuple[str, int]] = []

    def schedule(self, name: str, cb: Any, interval: int) -> None:
        self.scheduled.append((name, interval))
        cb(0)

    def cancel(self, name: str) -> None:
        pass


def test_health_monitor_polls_self_test() -> None:
    sched = DummyScheduler()
    with mock.patch('diagnostics.self_test', return_value={'system': {'disk_percent': 42}, 'network_ok': True, 'services': {}}):
        mon = diagnostics.HealthMonitor(cast(PollScheduler, sched), interval=5)
        assert sched.scheduled[0][0] == 'health_monitor'
        assert sched.scheduled[0][1] == 5
        assert mon.data is not None
        assert mon.data['system']['disk_percent'] == 42
