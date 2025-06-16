"""Tests for system diagnostics helpers."""
import os
import sys
import gzip
from unittest import mock
from types import ModuleType

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
aiohttp_mod = ModuleType('aiohttp')
aiohttp_mod.ClientSession = object
aiohttp_mod.ClientTimeout = lambda *a, **k: None
aiohttp_mod.ClientError = Exception
sys.modules['aiohttp'] = aiohttp_mod
import diagnostics
from typing import Any


def test_generate_system_report_includes_temp(monkeypatch: Any) -> None:
    monkeypatch.setattr('diagnostics.psutil.cpu_percent', lambda interval: 1)
    monkeypatch.setattr('diagnostics.psutil.virtual_memory', lambda: mock.Mock(percent=2))
    monkeypatch.setattr('diagnostics.psutil.disk_usage', lambda path: mock.Mock(percent=3))
    monkeypatch.setattr('diagnostics.utils.get_cpu_temp', lambda: 42.0)
    result = diagnostics.generate_system_report()
    assert result['cpu_temp'] == 42.0

def test_self_test_returns_extra_info() -> None:
    mock_stats = {'eth0': mock.Mock(isup=True)}
    mock_usb_proc = mock.Mock(returncode=0, stdout='dev1\ndev2\n')
    sys_metrics = {'ok': True, 'cpu_temp': 50.0}
    with mock.patch('diagnostics.generate_system_report', return_value=sys_metrics), \
         mock.patch('diagnostics.run_network_test', return_value=True), \
         mock.patch('diagnostics.psutil.net_if_stats', return_value=mock_stats), \
         mock.patch('diagnostics.subprocess.run', return_value=mock_usb_proc), \
         mock.patch('diagnostics.utils.service_status', side_effect=[True, False, True]):
        result = diagnostics.self_test()
        assert result['interfaces'] == {'eth0': True}
        assert result['usb'] == ['dev1', 'dev2']
        assert result['services'] == {'kismet': True, 'bettercap': False, 'gpsd': True}


def test_stop_profiling_writes_callgrind(tmp_path: Any) -> None:
    path = tmp_path / 'out.callgrind'
    os.environ['PW_PROFILE_CALLGRIND'] = str(path)
    diagnostics.start_profiling()
    sum(range(10))
    summary = diagnostics.stop_profiling()
    assert summary is not None
    assert path.exists()
    os.environ.pop('PW_PROFILE_CALLGRIND')


def test_rotate_log_gz(tmp_path: Any) -> None:
    log = tmp_path / 'test.log'
    log.write_text('first')
    diagnostics.rotate_log(str(log), max_files=2)
    gz1 = tmp_path / 'test.log.1.gz'
    assert gz1.is_file()
    with gzip.open(gz1, 'rt') as fh:
        assert fh.read() == 'first'

    log.write_text('second')
    diagnostics.rotate_log(str(log), max_files=2)
    gz2 = tmp_path / 'test.log.2.gz'
    assert gz1.is_file()
    assert gz2.is_file()

    log.write_text('third')
    diagnostics.rotate_log(str(log), max_files=2)
    assert (tmp_path / 'test.log.3.gz').exists() is False


def test_run_network_test_caches_success(monkeypatch: Any) -> None:
    diagnostics._LAST_NETWORK_OK = None
    times = iter([0.0, 10.0])
    monkeypatch.setattr(diagnostics.time, "time", lambda: next(times))

    call_count = 0

    def fake_run(args, capture_output=True):
        nonlocal call_count
        call_count += 1
        return mock.Mock(returncode=0)

    monkeypatch.setattr(diagnostics.subprocess, "run", fake_run)

    assert diagnostics.run_network_test("example.com") is True
    assert call_count == 1
    assert diagnostics.run_network_test("example.com") is True
    assert call_count == 1


def test_run_network_test_cache_expires(monkeypatch: Any) -> None:
    diagnostics._LAST_NETWORK_OK = None
    times = iter([0.0, 40.0])
    monkeypatch.setattr(diagnostics.time, "time", lambda: next(times))

    call_count = 0

    def fake_run(args, capture_output=True):
        nonlocal call_count
        call_count += 1
        return mock.Mock(returncode=0)

    monkeypatch.setattr(diagnostics.subprocess, "run", fake_run)

    assert diagnostics.run_network_test("example.com") is True
    assert diagnostics.run_network_test("example.com") is True
    assert call_count == 2
