import sys
import os
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import diagnostics


class DummyScheduler:
    def __init__(self):
        self.scheduled = []

    def schedule(self, name, cb, interval):
        self.scheduled.append((name, interval))
        cb(0)

    def cancel(self, name):
        pass


def test_health_monitor_polls_self_test():
    sched = DummyScheduler()
    with mock.patch('diagnostics.self_test', return_value={'system': {'disk_percent': 42}, 'network_ok': True, 'services': {}}):
        mon = diagnostics.HealthMonitor(sched, interval=5)
        assert sched.scheduled[0][0] == 'health_monitor'
        assert sched.scheduled[0][1] == 5
        assert mon.data['system']['disk_percent'] == 42
