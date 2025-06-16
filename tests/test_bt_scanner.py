import os
import sys
from types import SimpleNamespace
import builtins

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sigint_suite.bluetooth.scanner import scan_bluetooth


class DummyDevice(SimpleNamespace):
    pass


def test_scan_bluetooth_bleak(monkeypatch):
    async def fake_discover(timeout=10):
        return [
            DummyDevice(address="AA:BB:CC:DD:EE:FF", name="Foo"),
            DummyDevice(address="11:22:33:44:55:66", name=None),
        ]

    monkeypatch.setattr("bleak.BleakScanner.discover", fake_discover)

    devices = scan_bluetooth(timeout=1)
    assert devices == [
        {"address": "AA:BB:CC:DD:EE:FF", "name": "Foo"},
        {"address": "11:22:33:44:55:66", "name": "11:22:33:44:55:66"},
    ]


def test_scan_bluetooth_fallback(monkeypatch):
    output = """[NEW] Device AA:BB:CC:DD:EE:FF Foo\n[NEW] Device 11:22:33:44:55:66 Bar"""
    monkeypatch.setattr("subprocess.check_output", lambda *a, **k: output)

    orig_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "bleak":
            raise ModuleNotFoundError
        return orig_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    devices = scan_bluetooth(timeout=1)
    assert {"address": "AA:BB:CC:DD:EE:FF", "name": "Foo"} in devices
    assert {"address": "11:22:33:44:55:66", "name": "Bar"} in devices

