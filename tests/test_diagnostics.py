"""Tests for system diagnostics helpers."""
import os
import sys
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
