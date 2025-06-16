"""Tests for various utility helpers."""
import os
import sys
import tempfile
import zipfile
import json
import logging

from typing import Any
from pathlib import Path
from types import ModuleType
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import persistence

from unittest import mock
import types
sys.modules.setdefault('psutil', mock.Mock())
aiohttp_mod = types.SimpleNamespace(
    ClientSession=object,
    ClientError=Exception,
    ClientTimeout=lambda *a, **k: None,
)
sys.modules['aiohttp'] = aiohttp_mod
import psutil
if 'requests' not in sys.modules:
    dummy_requests = mock.Mock()
    dummy_requests.RequestException = Exception
    sys.modules['requests'] = dummy_requests
import utils
from collections import namedtuple


def test_format_error_with_enum() -> None:
    msg = utils.format_error(utils.ErrorCode.KISMET_API_ERROR, "fail")
    assert msg == "[E303] fail"


def test_find_latest_file_returns_latest() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = os.path.join(tmpdir, 'a.txt')
        file2 = os.path.join(tmpdir, 'b.txt')
        with open(file1, 'w') as f:
            f.write('1')
        with open(file2, 'w') as f:
            f.write('2')
        os.utime(file1, (1, 1))
        os.utime(file2, (2, 2))
        result = utils.find_latest_file(tmpdir, '*.txt')
        assert result == file2


def test_find_latest_file_none_when_empty() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        assert utils.find_latest_file(tmpdir, '*.txt') is None


def test_tail_file_returns_last_lines() -> None:
    with tempfile.NamedTemporaryFile('w+', delete=False) as tmp:
        for i in range(5):
            tmp.write(f"line{i}\n")
        tmp_path = tmp.name
    try:
        result = utils.tail_file(tmp_path, lines=3)
        assert result == ['line2', 'line3', 'line4']
    finally:
        os.unlink(tmp_path)


def test_tail_file_missing_returns_empty_list() -> None:
    result = utils.tail_file('/does/not/exist', lines=3)
    assert result == []


def test_tail_file_handles_large_file(tmp_path: Any) -> None:
    path = tmp_path / 'large.txt'
    with open(path, 'w') as f:
        for i in range(1000):
            f.write(f'line{i}\n')

    result = utils.tail_file(str(path), lines=5)
    assert result == [f'line{i}' for i in range(995, 1000)]


def _patch_dbus(monkeypatch: Any, manager: Any, props: Any) -> None:
    class Bus:
        def __init__(self, *a: Any, **k: Any) -> None:
            pass
        async def connect(self) -> None:
            pass

        async def introspect(self, service: str, path: str) -> str:
            return "intro"

        def get_proxy_object(self, service: str, path: str, _intro: str) -> Any:
            class Obj:
                def get_interface(self, iface: str) -> Any:
                    return manager if "Manager" in iface else props

            return Obj()

        def disconnect(self) -> None:
            pass

    aio_mod = types.SimpleNamespace(MessageBus=Bus)
    dbus_mod = types.SimpleNamespace(aio=aio_mod, BusType=types.SimpleNamespace(SYSTEM=1))
    monkeypatch.setitem(sys.modules, 'dbus_fast', dbus_mod)
    monkeypatch.setitem(sys.modules, 'dbus_fast.aio', aio_mod)


def _patch_bt_dbus(monkeypatch: Any, objects: dict[str, Any], exc: bool = False) -> None:
    class Bus:
        def get_object(self, service: str, path: str) -> Any:
            return 'bluez'

    class Manager:
        def GetManagedObjects(self) -> dict[str, Any]:
            if exc:
                raise Exception('boom')
            return objects

    def system_bus() -> Bus:
        return Bus()

    def interface(_obj: str, iface: str) -> Any:
        return Manager()

    dbus_mod = types.SimpleNamespace(SystemBus=system_bus, Interface=interface, DBusException=Exception)
    monkeypatch.setitem(sys.modules, 'dbus', dbus_mod)


def test_run_service_cmd_success(monkeypatch: Any) -> None:
    mgr = mock.Mock(call_start_unit=mock.AsyncMock())
    props = mock.Mock()
    _patch_dbus(monkeypatch, mgr, props)

    success, out, err = utils.run_service_cmd('kismet', 'start')
    mgr.call_start_unit.assert_called_once_with('kismet.service', 'replace')
    assert success is True and out == '' and err == ''


def test_run_service_cmd_failure(monkeypatch: Any) -> None:
    mgr = mock.Mock(call_start_unit=mock.AsyncMock(side_effect=Exception('err')))
    props = mock.Mock()
    _patch_dbus(monkeypatch, mgr, props)

    success, out, err = utils.run_service_cmd('kismet', 'start')
    mgr.call_start_unit.assert_called_once()
    assert success is False and out == '' and 'err' in err


def test_run_service_cmd_retries_until_success(monkeypatch: Any) -> None:
    calls = [OSError('boom'), None]

    def start_side(*_a: Any, **_k: Any) -> None:
        res = calls.pop(0)
        if isinstance(res, Exception):
            raise res

    mgr = mock.Mock(call_start_unit=mock.AsyncMock(side_effect=start_side))
    props = mock.Mock()
    _patch_dbus(monkeypatch, mgr, props)

    success, out, err = utils.run_service_cmd('kismet', 'start', attempts=2, delay=0)
    assert mgr.call_start_unit.call_count == 2
    assert success is True and out == '' and err == ''


def test_service_status_passes_retry_params() -> None:
    async def _svc(_: str, attempts: int = 1, delay: float = 0) -> bool:
        assert attempts == 2 and delay == 0.5
        return True

    with mock.patch('utils.service_status_async', _svc):
        assert utils.service_status('kismet', attempts=2, delay=0.5) is True


def test_point_in_polygon_basic() -> None:
    square = [(0, 0), (0, 1), (1, 1), (1, 0)]
    assert utils.point_in_polygon((0.5, 0.5), square) is True
    assert utils.point_in_polygon((1.5, 0.5), square) is False


def test_load_kml_parses_features(tmp_path: Any) -> None:
    kml_content = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<kml xmlns='http://www.opengis.net/kml/2.2'>"
        "<Placemark><name>Line</name><LineString><coordinates>0,0 1,1</coordinates></LineString></Placemark>"
        "<Placemark><name>Pt</name><Point><coordinates>2,2</coordinates></Point></Placemark>"
        "</kml>"
    )
    kml_path = tmp_path / 'test.kml'
    kml_path.write_text(kml_content)
    feats = utils.load_kml(str(kml_path))
    types = sorted(f['type'] for f in feats)
    assert types == ['LineString', 'Point']


def test_load_kmz_parses_features(tmp_path: Any) -> None:
    kml_content = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<kml xmlns='http://www.opengis.net/kml/2.2'>"
        "<Placemark><name>Pt</name><Point><coordinates>3,3</coordinates></Point></Placemark>"
        "</kml>"
    )
    kmz_path = tmp_path / 'test.kmz'
    with zipfile.ZipFile(kmz_path, 'w') as zf:
        zf.writestr('doc.kml', kml_content)
    feats = utils.load_kml(str(kmz_path))
    assert feats and feats[0]['type'] == 'Point'


def test_fetch_kismet_devices_request_exception(monkeypatch: Any) -> None:
    class FakeSession:
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass
        def get(self, _url: str, **_k: Any):
            raise utils.aiohttp.ClientError("boom")

    monkeypatch.setattr(utils.aiohttp, "ClientSession", lambda *a, **k: FakeSession())

    with mock.patch("utils.report_error") as err:
        aps, clients = utils.fetch_kismet_devices()
        assert aps == [] and clients == []
        assert err.call_count == 2


def test_fetch_kismet_devices_json_error(monkeypatch: Any) -> None:
    class FakeResp:
        status = 200

        async def text(self) -> str:
            return "invalid json"

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

    class FakeSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        def get(self, _url: str, **_k: Any) -> FakeResp:
            return FakeResp()

    monkeypatch.setattr(utils.aiohttp, "ClientSession", lambda *a, **k: FakeSession())

    with mock.patch("utils.report_error") as err:
        aps, clients = utils.fetch_kismet_devices()
        assert aps == [] and clients == []
        assert err.call_count == 2


def test_get_smart_status_ok(monkeypatch: Any) -> None:
    Part = namedtuple('Part', 'device mountpoint fstype opts')
    part = Part('/dev/sda', '/mnt/ssd', 'ext4', '')
    monkeypatch.setattr(psutil, 'disk_partitions', lambda all=False: [part])
    proc = mock.Mock(returncode=0, stdout='SMART overall-health self-assessment test result: PASSED\n', stderr='')
    monkeypatch.setattr(utils.subprocess, 'run', lambda *a, **k: proc)
    assert utils.get_smart_status('/mnt/ssd') == 'OK'


def test_fetch_kismet_devices_async(monkeypatch: Any) -> None:
    class FakeResp:
        status = 200

        async def text(self) -> str:
            return '{"access_points": [1], "clients": [2]}'

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

    class FakeSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        def get(self, _url: str, **_k: Any) -> FakeResp:
            return FakeResp()

    monkeypatch.setattr(utils.aiohttp, "ClientSession", lambda *a, **k: FakeSession())

    aps, clients = asyncio.run(utils.fetch_kismet_devices_async())
    assert aps == [1] and clients == [2]


def test_fetch_kismet_devices_cache(monkeypatch: Any, tmp_path: Path) -> None:
    os.environ["PW_DB_PATH"] = str(tmp_path / "app.db")

    asyncio.run(persistence.save_ap_cache([
        {
            "bssid": "AA",
            "ssid": "Test",
            "encryption": "WPA",
            "lat": 1.0,
            "lon": 2.0,
            "last_time": 1,
        }
    ]))

    class FakeSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        def get(self, _url: str, **_k: Any):
            raise utils.aiohttp.ClientError("boom")

    monkeypatch.setattr(utils.aiohttp, "ClientSession", lambda *a, **k: FakeSession())

    aps, clients = utils.fetch_kismet_devices()
    assert aps and aps[0]["bssid"] == "AA"
    assert clients == []


def test_safe_request_retries(monkeypatch: Any) -> None:
    calls: list[str] = []

    class Resp:
        status_code = 200
        content = b"{}"

        def raise_for_status(self) -> None:
            pass

    def get(url: str, timeout: int = 5) -> Resp:
        calls.append(url)
        if len(calls) == 1:
            raise utils.requests.RequestException("boom")
        return Resp()

    monkeypatch.setattr(utils, "requests", mock.Mock(get=get, RequestException=Exception))
    with mock.patch.object(utils, "report_error") as rep:
        resp = utils.safe_request("http://x")
        assert resp is not None
        assert rep.call_count == 0
    assert calls == ["http://x", "http://x"]


def test_ensure_service_running_attempts_restart(monkeypatch: Any) -> None:
    states = [False, True]

    def status(_svc: str) -> bool:
        return states.pop(0)

    monkeypatch.setattr(utils, "service_status", status)
    monkeypatch.setattr(
        utils,
        "run_service_cmd",
        lambda *a, **k: (True, "", ""),
    )
    with mock.patch.object(utils, "report_error") as rep:
        assert utils.ensure_service_running("svc") is True
        rep.assert_called_once()


def test_scan_bt_devices_parses_output(monkeypatch: Any) -> None:
    bt_mod = ModuleType("bluetooth")
    bt_mod.discover_devices = lambda *a, **k: [("AA:BB:CC:DD:EE:FF", "Foo")]
    monkeypatch.setitem(sys.modules, "bluetooth", bt_mod)

    class Props:
        def Get(self, iface: str, prop: str) -> str:
            assert iface == "org.bluez.Device1" and prop == "GPSCoordinates"
            return "1.0,2.0"

    class Bus:
        def get_object(self, service: str, path: str) -> str:
            return "dev"

    def interface(obj: str, iface: str) -> Props:
        return Props()

    dbus_mod = types.SimpleNamespace(SystemBus=lambda: Bus(), Interface=interface, DBusException=Exception)
    monkeypatch.setitem(sys.modules, "dbus", dbus_mod)


    objs = {
        "/dev": {
            "org.bluez.Device1": {
                "Address": "AA:BB:CC:DD:EE:FF",
                "Name": "Foo",
                "GPS Coordinates": "1.0,2.0",
            }
        }
    }

    _patch_bt_dbus(monkeypatch, objs)

    devices = utils.scan_bt_devices()
    assert [d.model_dump() for d in devices] == [
        {"address": "AA:BB:CC:DD:EE:FF", "name": "Foo", "lat": 1.0, "lon": 2.0}
    ]


def test_scan_bt_devices_handles_error(monkeypatch: Any) -> None:
    bt_mod = ModuleType("bluetooth")
    bt_mod.discover_devices = mock.Mock(side_effect=OSError())
    monkeypatch.setitem(sys.modules, "bluetooth", bt_mod)

    _patch_bt_dbus(monkeypatch, {}, exc=True)

    assert utils.scan_bt_devices() == []


def test_gpsd_cache(monkeypatch: Any) -> None:
    acc_mock = mock.Mock(side_effect=[2, 5])
    fix_mock = mock.Mock(side_effect=["2D", "3D"])

    monkeypatch.setattr(utils.gps_client, "get_accuracy", acc_mock)
    monkeypatch.setattr(utils.gps_client, "get_fix_quality", fix_mock)

    utils._GPSD_CACHE = {"timestamp": 0.0, "accuracy": None, "fix": "Unknown"}

    assert utils.get_gps_accuracy() == 2
    assert utils.get_gps_fix_quality() == "2D"
    assert acc_mock.call_count == 1  # gpsd queried once
    assert fix_mock.call_count == 1

    assert utils.get_gps_fix_quality(force_refresh=True) == "3D"
    assert acc_mock.call_count == 2
    assert fix_mock.call_count == 2


def test_count_bettercap_handshakes(tmp_path: Any) -> None:
    log_dir = tmp_path
    d1 = log_dir / "2024-01-01_bettercap"
    d2 = log_dir / "2024-01-02_bettercap"
    other = log_dir / "misc"
    d1.mkdir()
    d2.mkdir()
    other.mkdir()
    (d1 / "a.pcap").write_text("x")
    (d1 / "ignore.txt").write_text("x")
    (d2 / "b.pcap").write_text("x")
    (other / "c.pcap").write_text("x")
    assert utils.count_bettercap_handshakes(str(log_dir)) == 2


def test_count_bettercap_handshakes_missing(tmp_path: Any) -> None:
    missing = tmp_path / "nope"
    assert utils.count_bettercap_handshakes(str(missing)) == 0


def test_network_scanning_disabled(monkeypatch: Any) -> None:
    monkeypatch.setenv("PW_DISABLE_SCANNING", "1")
    assert utils.network_scanning_disabled() is True
    monkeypatch.delenv("PW_DISABLE_SCANNING")


def test_network_scanning_disabled_logs(monkeypatch: Any, caplog: Any) -> None:
    monkeypatch.setenv("PW_DISABLE_SCANNING", "1")
    with caplog.at_level(logging.DEBUG):
        assert utils.network_scanning_disabled() is True
    assert "Network scanning disabled" in caplog.text
    monkeypatch.delenv("PW_DISABLE_SCANNING")

