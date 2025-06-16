import sys
import os
from unittest import mock
from typing import Any, cast
from pathlib import Path
import time
from types import ModuleType

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # noqa: E402
aiohttp_mod = ModuleType('aiohttp')
aiohttp_mod.ClientSession = object
aiohttp_mod.ClientTimeout = lambda *a, **k: None
aiohttp_mod.ClientError = Exception
sys.modules['aiohttp'] = aiohttp_mod
import diagnostics  # noqa: E402
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
    with mock.patch('diagnostics.self_test', return_value={'system': {'disk_percent': 42}, 'network_ok': True, 'services': {}}), \
         mock.patch('diagnostics.purge_old_health') as purge, \
         mock.patch('diagnostics.vacuum') as vac:
        mon = diagnostics.HealthMonitor(cast(PollScheduler, sched), interval=5)
        assert sched.scheduled[0][0] == 'health_monitor'
        assert sched.scheduled[0][1] == 5
        assert mon.data is not None
        assert mon.data['system']['disk_percent'] == 42
        purge.assert_called_with(30)
        assert vac.call_count >= 1


def test_health_monitor_daily_summary() -> None:
    sched = DummyScheduler()
    with mock.patch(
        'diagnostics.self_test',
        return_value={'system': {'disk_percent': 42}, 'network_ok': True, 'services': {}},
    ), mock.patch('diagnostics.load_recent_health', return_value=[]):
        diagnostics.HealthMonitor(cast(PollScheduler, sched), interval=5, daily_summary=True)
        assert any(name == 'health_summary' and interval == 86400 for name, interval in sched.scheduled)


def test_health_monitor_exports(tmp_path, monkeypatch) -> None:
    sched = DummyScheduler()
    monkeypatch.setattr(diagnostics.config, "HEALTH_EXPORT_DIR", str(tmp_path))
    monkeypatch.setattr(diagnostics.config, "HEALTH_EXPORT_INTERVAL", 1)
    monkeypatch.setattr(diagnostics.config, "COMPRESS_HEALTH_EXPORTS", False)
    monkeypatch.setattr(diagnostics.config, "HEALTH_EXPORT_RETENTION", 1)
    created = {}

    def fake_export(args: list[str]) -> None:
        created["path"] = args[0]
        Path(args[0]).write_text("x")

    with mock.patch(
        'diagnostics.self_test',
        return_value={'system': {}, 'network_ok': True, 'services': {}},
    ), mock.patch('scripts.health_export.main', side_effect=fake_export):
        diagnostics.HealthMonitor(cast(PollScheduler, sched), interval=1)
        assert any(n == 'health_export' for n, _ in sched.scheduled)
        assert Path(created["path"]).exists()


def test_health_monitor_export_cleanup(tmp_path, monkeypatch) -> None:
    sched = DummyScheduler()
    monkeypatch.setattr(diagnostics.config, "HEALTH_EXPORT_DIR", str(tmp_path))
    monkeypatch.setattr(diagnostics.config, "HEALTH_EXPORT_INTERVAL", 1)
    monkeypatch.setattr(diagnostics.config, "COMPRESS_HEALTH_EXPORTS", True)
    monkeypatch.setattr(diagnostics.config, "HEALTH_EXPORT_RETENTION", 1)
    old = tmp_path / "old.json"
    old.write_text("y")
    os.utime(old, (time.time() - 172800, time.time() - 172800))

    def fake_export(args: list[str]) -> None:
        Path(args[0]).write_text("z")

    with mock.patch(
        'diagnostics.self_test',
        return_value={'system': {}, 'network_ok': True, 'services': {}},
    ), mock.patch('scripts.health_export.main', side_effect=fake_export):
        diagnostics.HealthMonitor(cast(PollScheduler, sched), interval=1)
        exported = list(tmp_path.glob('health_*.json.gz'))
        assert exported and exported[0].suffix == '.gz'
        assert not old.exists()
