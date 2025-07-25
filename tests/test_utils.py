"""Tests for various utility helpers."""

import asyncio
import logging
import os
import sys
import tempfile
import types
import zipfile
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest import mock

import pytest
import requests
import requests_cache
from cachetools import TTLCache

from piwardrive import persistence

sys.modules.setdefault("psutil", mock.Mock())
aiohttp_mod = types.SimpleNamespace(
    ClientSession=object,
    ClientError=Exception,
    ClientTimeout=lambda *a, **k: None,
)
sys.modules["aiohttp"] = aiohttp_mod
import psutil

if "requests" not in sys.modules:
    dummy_requests = mock.Mock()
    dummy_requests.RequestException = Exception
    sys.modules["requests"] = dummy_requests
from collections import namedtuple

from piwardrive import utils


def test_format_error_with_enum() -> None:
    msg = utils.format_error(utils.ErrorCode.KISMET_API_ERROR, "fail")
    assert msg == "[E303] fail"


def test_find_latest_file_returns_latest() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = os.path.join(tmpdir, "a.txt")
        file2 = os.path.join(tmpdir, "b.txt")
        with open(file1, "w") as f:
            f.write("1")
        with open(file2, "w") as f:
            f.write("2")
        os.utime(file1, (1, 1))
        os.utime(file2, (2, 2))
        result = utils.find_latest_file(tmpdir, "*.txt")
        assert result == file2


def test_find_latest_file_none_when_empty() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        assert utils.find_latest_file(tmpdir, "*.txt") is None


def test_tail_file_returns_last_lines() -> None:
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        for i in range(5):
            tmp.write(f"line{i}\n")
        tmp_path = tmp.name
    try:
        result = utils.tail_file(tmp_path, lines=3)
        assert result == ["line2", "line3", "line4"]
    finally:
        os.unlink(tmp_path)


def test_tail_file_missing_returns_empty_list() -> None:
    result = utils.tail_file("/does/not/exist", lines=3)
    assert result == []


def test_tail_file_nonpositive_lines() -> None:
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write("line0\nline1\n")
        tmp_path = tmp.name
    try:
        assert utils.tail_file(tmp_path, lines=0) == []
        assert utils.tail_file(tmp_path, lines=-1) == []
    finally:
        os.unlink(tmp_path)


def test_tail_file_handles_large_file(tmp_path: Any) -> None:
    path = tmp_path / "large.txt"
    with open(path, "w") as f:
        for i in range(1000):
            f.write(f"line{i}\n")

    result = utils.tail_file(str(path), lines=5)
    assert result == [f"line{i}" for i in range(995, 1000)]


def test_tail_file_cache(monkeypatch: Any, tmp_path: Any) -> None:
    path = tmp_path / "test.log"
    path.write_text("A\nB\n")
    utils._TAIL_FILE_CACHE.clear()
    assert utils.tail_file(str(path), lines=1) == ["B"]

    called = False

    def fail(*_a: Any, **_k: Any) -> Any:
        nonlocal called
        called = True
        raise AssertionError("open called")

    monkeypatch.setattr("piwardrive.core.utils.open", fail)
    monkeypatch.setattr(utils.os.path, "getmtime", lambda _p: path.stat().st_mtime)
    assert utils.tail_file(str(path), lines=1) == ["B"]
    assert not called


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
    dbus_mod = types.SimpleNamespace(
        aio=aio_mod, BusType=types.SimpleNamespace(SYSTEM=1)
    )
    monkeypatch.setitem(sys.modules, "dbus_fast", dbus_mod)
    monkeypatch.setitem(sys.modules, "dbus_fast.aio", aio_mod)


def _patch_bt_dbus(
    monkeypatch: Any, objects: dict[str, Any], exc: bool = False
) -> None:
    class Bus:
        def get_object(self, service: str, path: str) -> Any:
            return "bluez"

    class Manager:
        def GetManagedObjects(self) -> dict[str, Any]:
            if exc:
                raise Exception("boom")
            return objects

    def system_bus() -> Bus:
        return Bus()

    def interface(_obj: str, iface: str) -> Any:
        return Manager()

    dbus_mod = types.SimpleNamespace(
        SystemBus=system_bus, Interface=interface, DBusException=Exception
    )
    monkeypatch.setitem(sys.modules, "dbus", dbus_mod)


def test_run_service_cmd_success(monkeypatch: Any) -> None:
    mgr = mock.Mock(call_start_unit=mock.AsyncMock())
    props = mock.Mock()
    _patch_dbus(monkeypatch, mgr, props)

    success, out, err = utils.run_service_cmd("kismet", "start")
    mgr.call_start_unit.assert_called_once_with("kismet.service", "replace")
    assert success is True and out == "" and err == ""


def test_run_service_cmd_failure(monkeypatch: Any) -> None:
    mgr = mock.Mock(call_start_unit=mock.AsyncMock(side_effect=Exception("err")))
    props = mock.Mock()
    _patch_dbus(monkeypatch, mgr, props)

    success, out, err = utils.run_service_cmd("kismet", "start")
    mgr.call_start_unit.assert_called_once()
    assert success is False and out == "" and "err" in err


def test_run_service_cmd_retries_until_success(monkeypatch: Any) -> None:
    calls = [OSError("boom"), None]

    def start_side(*_a: Any, **_k: Any) -> None:
        res = calls.pop(0)
        if isinstance(res, Exception):
            raise res

    mgr = mock.Mock(call_start_unit=mock.AsyncMock(side_effect=start_side))
    props = mock.Mock()
    _patch_dbus(monkeypatch, mgr, props)

    success, out, err = utils.run_service_cmd("kismet", "start", attempts=2, delay=0)
    assert mgr.call_start_unit.call_count == 2
    assert success is True and out == "" and err == ""


def test_message_bus_disconnect_called(monkeypatch: Any) -> None:
    called = False

    class Bus:
        def __init__(self, *_a: Any, **_k: Any) -> None:
            pass

        async def connect(self) -> None:  # pragma: no cover - mock
            pass

        async def introspect(
            self, service: str, path: str
        ) -> str:  # pragma: no cover - mock
            return "intro"

        def get_proxy_object(self, service: str, path: str, _intro: str) -> Any:
            class Obj:
                def get_interface(self, iface: str) -> Any:
                    return mgr if "Manager" in iface else props

            return Obj()

        def disconnect(self) -> None:
            nonlocal called
            called = True

    mgr = mock.Mock(call_start_unit=mock.AsyncMock())
    props = mock.Mock()
    aio_mod = types.SimpleNamespace(MessageBus=Bus)
    dbus_mod = types.SimpleNamespace(
        aio=aio_mod, BusType=types.SimpleNamespace(SYSTEM=1)
    )
    monkeypatch.setitem(sys.modules, "dbus_fast", dbus_mod)
    monkeypatch.setitem(sys.modules, "dbus_fast.aio", aio_mod)

    success, _out, _err = utils.run_service_cmd("kismet", "start")
    assert success is True and called is True


def test_service_status_passes_retry_params() -> None:
    async def _svc(_: str, attempts: int = 1, delay: float = 0) -> bool:
        assert attempts == 2 and delay == 0.5
        return True

    with mock.patch("utils.service_status_async", _svc):
        assert utils.service_status("kismet", attempts=2, delay=0.5) is True


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
    kml_path = tmp_path / "test.kml"
    kml_path.write_text(kml_content)
    feats = utils.load_kml(str(kml_path))
    types = sorted(f["type"] for f in feats)
    assert types == ["LineString", "Point"]


def test_load_kmz_parses_features(tmp_path: Any) -> None:
    kml_content = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<kml xmlns='http://www.opengis.net/kml/2.2'>"
        "<Placemark><name>Pt</name><Point><coordinates>3,3</coordinates></Point></Placemark>"
        "</kml>"
    )
    kmz_path = tmp_path / "test.kmz"
    with zipfile.ZipFile(kmz_path, "w") as zf:
        zf.writestr("doc.kml", kml_content)
    feats = utils.load_kml(str(kmz_path))
    assert feats and feats[0]["type"] == "Point"


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
    Part = namedtuple("Part", "device mountpoint fstype opts")
    part = Part("/dev/sda", "/mnt/ssd", "ext4", "")
    monkeypatch.setattr(psutil, "disk_partitions", lambda all=False: [part])
    proc = mock.Mock(
        returncode=0,
        stdout="SMART overall-health self-assessment test result: PASSED\n",
        stderr="",
    )
    monkeypatch.setattr(utils.subprocess, "run", lambda *a, **k: proc)
    assert utils.get_smart_status("/mnt/ssd") == "OK"


def test_get_smart_status_failure(monkeypatch: Any) -> None:
    Part = namedtuple("Part", "device mountpoint fstype opts")
    part = Part("/dev/sda", "/mnt/ssd", "ext4", "")
    monkeypatch.setattr(psutil, "disk_partitions", lambda all=False: [part])
    monkeypatch.setattr(
        utils.subprocess,
        "run",
        lambda *a, **k: (_ for _ in ()).throw(
            utils.subprocess.CalledProcessError(1, "smartctl")
        ),
    )
    assert utils.get_smart_status("/mnt/ssd") is None


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


def test_fetch_kismet_devices_async_logs_cache_error(monkeypatch: Any) -> None:
    class FakeResp:
        status = 200

        async def text(self) -> str:
            return '{"access_points": [], "clients": []}'

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
    monkeypatch.setattr(
        persistence,
        "save_ap_cache",
        mock.AsyncMock(side_effect=Exception("fail")),
    )

    with mock.patch.object(utils.logging, "exception") as exc_log:
        asyncio.run(utils.fetch_kismet_devices_async())
        exc_log.assert_called_once()


def test_fetch_kismet_devices_cache(monkeypatch: Any, tmp_path: Path) -> None:
    os.environ["PW_DB_PATH"] = str(tmp_path / "app.db")

    asyncio.run(
        persistence.save_ap_cache(
            [
                {
                    "bssid": "AA",
                    "ssid": "Test",
                    "encryption": "WPA",
                    "lat": 1.0,
                    "lon": 2.0,
                    "last_time": 1,
                }
            ]
        )
    )

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


def test_fetch_kismet_devices_async_cache(monkeypatch: Any) -> None:
    calls: list[int] = []

    class FakeResp:
        status = 200

        async def text(self) -> str:
            return '{"access_points": [], "clients": []}'

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
            calls.append(1)
            return FakeResp()

    monkeypatch.setattr(utils.aiohttp, "ClientSession", lambda *a, **k: FakeSession())
    monkeypatch.setattr(persistence, "save_ap_cache", mock.AsyncMock())
    times = [0.0, 1.0, 3.5]
    monkeypatch.setattr(utils.time, "time", lambda: times.pop(0))

    asyncio.run(utils.fetch_kismet_devices_async())
    asyncio.run(utils.fetch_kismet_devices_async())
    assert len(calls) == 1
    asyncio.run(utils.fetch_kismet_devices_async())
    assert len(calls) == 2


def test_safe_request_retries(monkeypatch: Any) -> None:
    calls: list[str] = []

    class Resp:
        status_code = 200
        content = b"{}"

        def raise_for_status(self) -> None:
            pass

    def get(
        url: str, timeout: int = 5, expire_after=None
    ) -> Resp:  # type: ignore[override]
        calls.append(url)
        if len(calls) == 1:
            raise Exception("boom")
        return Resp()

    monkeypatch.setattr(utils.HTTP_SESSION, "get", get)
    with mock.patch.object(utils, "report_error") as rep:
        resp = utils.safe_request("http://x")
        assert resp is not None
        assert rep.call_count == 0
    assert calls == ["http://x", "http://x"]


def test_safe_request_cache(monkeypatch: Any) -> None:
    calls: list[str] = []

    class Resp:
        status_code = 200

        def raise_for_status(self) -> None:
            pass

    session = requests_cache.CachedSession(backend="memory", expire_after=5)

    def request(url: str, *args: Any, **_kw: Any) -> Resp:
        calls.append(url)
        return Resp()

    session.get = request  # type: ignore[assignment]
    monkeypatch.setattr(utils, "HTTP_SESSION", session)
    import piwardrive.core.utils as core_utils

    monkeypatch.setattr(core_utils, "HTTP_SESSION", session)
    utils._SAFE_REQUEST_CACHE = TTLCache(maxsize=128, ttl=5)
    core_utils._SAFE_REQUEST_CACHE = utils._SAFE_REQUEST_CACHE

    first = utils.safe_request("http://x", cache_seconds=5)
    second = utils.safe_request("http://x", cache_seconds=5)
    assert first is second
    assert calls == ["http://x"]


def test_safe_request_cache_pruning(monkeypatch: Any) -> None:
    class Resp:
        status_code = 200

        def raise_for_status(self) -> None:
            pass

    def get(_url: str, timeout: int = 5, expire_after=None, **_kw: Any) -> Resp:
        return Resp()

    monkeypatch.setattr(utils, "HTTP_SESSION", mock.Mock(get=get))
    monkeypatch.setattr(
        utils,
        "requests",
        mock.Mock(Timeout=Exception, HTTPError=Exception, RequestException=Exception),
    )
    import piwardrive.core.utils as core_utils

    monkeypatch.setattr(core_utils, "HTTP_SESSION", utils.HTTP_SESSION)
    monkeypatch.setattr(core_utils, "requests", utils.requests)
    t = -1

    def timer() -> float:
        nonlocal t
        t += 1
        return float(t)

    utils._SAFE_REQUEST_CACHE = TTLCache(maxsize=1, ttl=5, timer=timer)
    core_utils._SAFE_REQUEST_CACHE = utils._SAFE_REQUEST_CACHE
    monkeypatch.setattr(utils, "SAFE_REQUEST_CACHE_MAX_SIZE", 1)

    utils.safe_request("http://a")
    utils.safe_request("http://b")

    assert "http://a" not in utils._SAFE_REQUEST_CACHE
    assert "http://b" in utils._SAFE_REQUEST_CACHE


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

    dbus_mod = types.SimpleNamespace(
        SystemBus=lambda: Bus(), Interface=interface, DBusException=Exception
    )
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
    acc_mock = mock.Mock(side_effect=[2, None, 5])
    fix_mock = mock.Mock(side_effect=["2D", "Unknown", "3D"])

    monkeypatch.setattr(utils.gps_client, "get_accuracy", acc_mock)
    monkeypatch.setattr(utils.gps_client, "get_fix_quality", fix_mock)

    utils._GPSD_CACHE = {"timestamp": 0.0, "accuracy": None, "fix": "Unknown"}

    assert utils.get_gps_accuracy() == 2
    assert utils.get_gps_fix_quality() == "2D"
    assert acc_mock.call_count == 1  # gpsd queried once
    assert fix_mock.call_count == 1

    ts_first = utils._GPSD_CACHE["timestamp"]

    # failure should not overwrite timestamp or cached data
    assert utils.get_gps_accuracy(force_refresh=True) == 2
    assert utils._GPSD_CACHE["timestamp"] == ts_first
    assert acc_mock.call_count == 2
    assert fix_mock.call_count == 2

    assert utils.get_gps_fix_quality(force_refresh=True) == "3D"
    assert utils._GPSD_CACHE["timestamp"] > ts_first
    assert acc_mock.call_count == 3
    assert fix_mock.call_count == 3


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


def test_count_bettercap_handshakes_cache(monkeypatch: Any, tmp_path: Any) -> None:
    log_dir = tmp_path
    d1 = log_dir / "2024-01-01_bettercap"
    d1.mkdir()
    (d1 / "a.pcap").write_text("x")

    monkeypatch.setattr(utils.time, "time", lambda: 1.0)
    utils._HANDSHAKE_CACHE.clear()
    assert utils.count_bettercap_handshakes(str(log_dir)) == 1

    (d1 / "b.pcap").write_text("x")
    monkeypatch.setattr(utils.time, "time", lambda: 5.0)
    assert utils.count_bettercap_handshakes(str(log_dir)) == 2

    monkeypatch.setattr(utils.time, "time", lambda: 12.0)
    assert utils.count_bettercap_handshakes(str(log_dir)) == 2


def test_network_scanning_disabled(monkeypatch: Any) -> None:
    monkeypatch.setenv("PW_DISABLE_SCANNING", "1")
    assert utils.network_scanning_disabled() is True
    monkeypatch.delenv("PW_DISABLE_SCANNING")


def test_get_network_throughput_interface(monkeypatch: Any) -> None:
    class C:
        def __init__(self, r: int, s: int) -> None:
            self.bytes_recv = r
            self.bytes_sent = s

    calls = [C(100, 200), C(200, 300)]

    def fake_counters(pernic: bool = False) -> Any:
        if pernic:
            return {"eth0": calls.pop(0)}
        return calls.pop(0)

    monkeypatch.setattr(utils.psutil, "net_io_counters", fake_counters)
    monkeypatch.setattr(utils.time, "time", lambda: 1.0)
    utils._NET_IO_CACHE.clear()
    utils.get_network_throughput("eth0")
    monkeypatch.setattr(utils.time, "time", lambda: 2.0)
    rx, tx = utils.get_network_throughput("eth0")
    assert rx == (200 - 100) / 1.0 / 1024.0
    assert tx == (300 - 200) / 1.0 / 1024.0


def test_network_scanning_disabled_logs(monkeypatch: Any, caplog: Any) -> None:
    monkeypatch.setenv("PW_DISABLE_SCANNING", "1")
    with caplog.at_level(logging.DEBUG):
        assert utils.network_scanning_disabled() is True
    assert "Network scanning disabled" in caplog.text
    monkeypatch.delenv("PW_DISABLE_SCANNING")


def test_get_network_throughput_calculates_kbps(monkeypatch: Any) -> None:
    net = namedtuple("Net", "bytes_sent bytes_recv")
    utils._NET_IO_CACHE = {"timestamp": 1.0, "counters": net(1000, 2000)}
    monkeypatch.setattr(utils.time, "time", lambda: 2.0)
    monkeypatch.setattr(psutil, "net_io_counters", lambda: net(3000, 6000))

    rx, tx = utils.get_network_throughput()

    assert round(rx, 2) == round((6000 - 2000) / 1024.0, 2)
    assert round(tx, 2) == round((3000 - 1000) / 1024.0, 2)
    assert utils._NET_IO_CACHE["counters"].bytes_recv == 6000
    assert utils._NET_IO_CACHE["timestamp"] == 2.0


def test_get_network_throughput_resets_when_cache_missing(monkeypatch: Any) -> None:
    net = namedtuple("Net", "bytes_sent bytes_recv")
    utils._NET_IO_CACHE = {}
    monkeypatch.setattr(psutil, "net_io_counters", lambda: net(500, 700))
    monkeypatch.setattr(utils.time, "time", lambda: 1.0)

    rx, tx = utils.get_network_throughput()

    assert rx == 0.0 and tx == 0.0
    assert utils._NET_IO_CACHE["counters"].bytes_sent == 500
    assert utils._NET_IO_CACHE["timestamp"] == 1.0


def test_run_async_task() -> None:
    """The async loop is started on demand and callbacks run."""
    import importlib
    import sys

    sys.modules.pop("utils", None)
    utils_mod = importlib.import_module("utils")

    async def do_work() -> int:
        return 3

    results: list[int] = []

    def cb(val: int) -> None:
        results.append(val)

    fut = utils_mod.run_async_task(do_work(), callback=cb)
    assert fut.result(timeout=1) == 3
    assert results == [3]
    utils_mod.shutdown_async_loop()


def test_get_mem_usage_cache(monkeypatch: Any) -> None:
    utils._MEM_USAGE_CACHE = {"timestamp": 0.0, "percent": None}

    monkeypatch.setattr(utils.time, "time", lambda: 1.0)
    monkeypatch.setattr(
        utils.psutil, "virtual_memory", lambda: types.SimpleNamespace(percent=40)
    )
    assert utils.get_mem_usage() == 40

    monkeypatch.setattr(utils.time, "time", lambda: 2.0)
    monkeypatch.setattr(
        utils.psutil, "virtual_memory", lambda: types.SimpleNamespace(percent=50)
    )
    assert utils.get_mem_usage() == 40

    monkeypatch.setattr(utils.time, "time", lambda: 4.5)
    assert utils.get_mem_usage() == 50


def test_get_disk_usage_cache(monkeypatch: Any) -> None:
    utils._DISK_USAGE_CACHE.clear()

    monkeypatch.setattr(utils.time, "time", lambda: 1.0)
    monkeypatch.setattr(
        utils.psutil, "disk_usage", lambda p: types.SimpleNamespace(percent=70)
    )
    assert utils.get_disk_usage("/mnt/ssd") == 70

    monkeypatch.setattr(utils.time, "time", lambda: 2.0)
    monkeypatch.setattr(
        utils.psutil, "disk_usage", lambda p: types.SimpleNamespace(percent=80)
    )
    assert utils.get_disk_usage("/mnt/ssd") == 70

    monkeypatch.setattr(utils.time, "time", lambda: 4.5)
    assert utils.get_disk_usage("/mnt/ssd") == 80


class TestRobustRequest:
    """Test the robust_request function with retries and exponential backoff."""

    def test_robust_request_success_first_attempt(self, monkeypatch: Any) -> None:
        """Test robust_request succeeds on first attempt."""
        mock_response = mock.Mock()
        mock_response.status_code = 200

        mock_request = mock.Mock(return_value=mock_response)
        monkeypatch.setattr("requests.request", mock_request)

        result = utils.robust_request("http://example.com")

        assert result == mock_response
        mock_request.assert_called_once_with(
            "GET", "http://example.com", headers=None, timeout=5.0
        )

    def test_robust_request_custom_parameters(self, monkeypatch: Any) -> None:
        """Test robust_request with custom method, headers, and timeout."""
        mock_response = mock.Mock()
        mock_request = mock.Mock(return_value=mock_response)
        monkeypatch.setattr("requests.request", mock_request)

        headers = {"Authorization": "Bearer token"}
        result = utils.robust_request(
            "http://example.com/api",
            method="POST",
            headers=headers,
            timeout=10.0,
        )

        assert result == mock_response
        mock_request.assert_called_once_with(
            "POST", "http://example.com/api", headers=headers, timeout=10.0
        )

    def test_robust_request_retries_on_exception(self, monkeypatch: Any) -> None:
        """Test robust_request retries on RequestException."""
        mock_response = mock.Mock()

        # Fail twice, then succeed
        call_count = 0

        def mock_request(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise requests.RequestException("Connection failed")
            return mock_response

        monkeypatch.setattr("requests.request", mock_request)
        monkeypatch.setattr("time.sleep", mock.Mock())  # Speed up test

        result = utils.robust_request("http://example.com")

        assert result == mock_response
        assert call_count == 3

    def test_robust_request_exhausts_retries(self, monkeypatch: Any) -> None:
        """Test robust_request raises exception after exhausting retries."""

        def mock_request(*args, **kwargs):
            raise requests.RequestException("Persistent failure")

        monkeypatch.setattr("requests.request", mock_request)
        monkeypatch.setattr("time.sleep", mock.Mock())  # Speed up test

        with pytest.raises(requests.RequestException, match="Persistent failure"):
            utils.robust_request("http://example.com")

    def test_robust_request_exponential_backoff(self, monkeypatch: Any) -> None:
        """Test robust_request uses exponential backoff for delays."""
        call_count = 0

        def mock_request(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise requests.RequestException("Always fail")

        sleep_calls = []

        def mock_sleep(delay):
            sleep_calls.append(delay)

        monkeypatch.setattr("requests.request", mock_request)
        monkeypatch.setattr("time.sleep", mock_sleep)

        with pytest.raises(requests.RequestException):
            utils.robust_request("http://example.com")

        # Should have called sleep with exponentially increasing delays
        assert len(sleep_calls) == 2  # 3 attempts = 2 sleeps
        assert sleep_calls[0] == 1  # First delay (RETRY_DELAY)
        assert sleep_calls[1] == 2  # Second delay (doubled)

    def test_robust_request_different_request_exceptions(
        self, monkeypatch: Any
    ) -> None:
        """Test robust_request handles different types of RequestException."""
        mock_response = mock.Mock()

        # Test various request exceptions
        exceptions_to_test = [
            requests.ConnectionError("Connection failed"),
            requests.Timeout("Request timed out"),
            requests.HTTPError("HTTP error"),
            requests.RequestException("Generic request error"),
        ]

        for exception in exceptions_to_test:
            call_count = 0

            def mock_request(*args, **kwargs):
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    raise exception
                return mock_response

            monkeypatch.setattr("requests.request", mock_request)
            monkeypatch.setattr("time.sleep", mock.Mock())

            result = utils.robust_request("http://example.com")
            assert result == mock_response

    def test_robust_request_logs_warnings(self, monkeypatch: Any, caplog: Any) -> None:
        """Test robust_request logs warnings for failed attempts."""
        call_count = 0

        def mock_request(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise requests.RequestException("Connection failed")
            return mock.Mock()

        monkeypatch.setattr("requests.request", mock_request)
        monkeypatch.setattr("time.sleep", mock.Mock())

        with caplog.at_level(logging.WARNING):
            utils.robust_request("http://example.com")

        # Should have logged warnings for the failed attempts
        warning_logs = [
            record for record in caplog.records if record.levelno == logging.WARNING
        ]
        assert len(warning_logs) == 2
        assert "Request failed" in warning_logs[0].message
        assert "Connection failed" in warning_logs[0].message
