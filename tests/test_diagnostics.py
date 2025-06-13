"""Tests for system diagnostics helpers."""
import os
import sys
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import diagnostics


def test_self_test_returns_extra_info():
    mock_stats = {'eth0': mock.Mock(isup=True)}
    mock_usb_proc = mock.Mock(returncode=0, stdout='dev1\ndev2\n')
    with mock.patch('diagnostics.generate_system_report', return_value={'ok': True}), \
         mock.patch('diagnostics.run_network_test', return_value=True), \
         mock.patch('diagnostics.psutil.net_if_stats', return_value=mock_stats), \
         mock.patch('diagnostics.subprocess.run', return_value=mock_usb_proc), \
         mock.patch('diagnostics.utils.service_status', side_effect=[True, False, True]):
        result = diagnostics.self_test()
        assert result['interfaces'] == {'eth0': True}
        assert result['usb'] == ['dev1', 'dev2']
        assert result['services'] == {'kismet': True, 'bettercap': False, 'gpsd': True}
