import asyncio
import json
import sys
import tempfile
from dataclasses import asdict
from types import ModuleType, SimpleNamespace
from typing import Any
from unittest import mock

import pytest
from fastapi import WebSocketDisconnect

aiohttp_mod = ModuleType("aiohttp")
aiohttp_mod.ClientSession = object  # type: ignore[attr-defined]
aiohttp_mod.ClientTimeout = lambda *a, **k: None  # type: ignore[attr-defined]
aiohttp_mod.ClientError = Exception  # type: ignore[attr-defined]
sys.modules["aiohttp"] = aiohttp_mod
utils_mod = ModuleType("utils")


async def _dummy_async(*_a, **_k):
    return None


utils_mod.fetch_metrics_async = _dummy_async
utils_mod.get_avg_rssi = lambda *a, **k: None
utils_mod.get_cpu_temp = lambda *a, **k: None
utils_mod.get_network_throughput = lambda *a, **k: None
utils_mod.get_gps_fix_quality = lambda *a, **k: None
utils_mod.service_status_async = _dummy_async
utils_mod.async_tail_file = _dummy_async
sys.modules["utils"] = utils_mod

from fastapi.testclient import TestClient  # noqa: E402

from piwardrive import persistence  # noqa: E402
from piwardrive import security  # noqa: E402
from piwardrive import service  # noqa: E402


def test_status_endpoint_returns_recent_records() -> None:
    rec = persistence.HealthRecord(
        timestamp="t",
        cpu_temp=1.0,
        cpu_percent=2.0,
        memory_percent=3.0,
        disk_percent=4.0,
    )

    async def _mock(_: int) -> list:
        return [rec]

    with (
        mock.patch("service.load_recent_health", _mock),
        mock.patch("piwardrive.service.load_recent_health", _mock),
    ):
        client = TestClient(service.app)
        resp = client.get("/status")
        assert resp.status_code == 200
        assert resp.json() == [asdict(rec)]


def test_widget_metrics_endpoint() -> None:
    async def fake_fetch() -> tuple[list, list, int]:
        return ([{"signal_dbm": -10}], [], 5)

    with (
        mock.patch("service.fetch_metrics_async", fake_fetch),
        mock.patch("piwardrive.service.fetch_metrics_async", fake_fetch),
        mock.patch("service.get_cpu_temp", return_value=40.0),
        mock.patch("piwardrive.service.get_cpu_temp", return_value=40.0),
        mock.patch("service.get_network_throughput", return_value=(1.0, 2.0)),
        mock.patch(
            "piwardrive.service.get_network_throughput", return_value=(1.0, 2.0)
        ),
        mock.patch("service.get_gps_fix_quality", return_value="3D"),
        mock.patch("piwardrive.service.get_gps_fix_quality", return_value="3D"),
        mock.patch("service.service_status_async", side_effect=[True, False]),
        mock.patch(
            "service.psutil.sensors_battery",
            return_value=SimpleNamespace(percent=75.0, power_plugged=True),
        ),
        mock.patch("service.vehicle_sensors.read_speed_obd", return_value=30.0),
        mock.patch("service.vehicle_sensors.read_rpm_obd", return_value=1500.0),
        mock.patch("service.vehicle_sensors.read_engine_load_obd", return_value=50.0),
    ):
        client = TestClient(service.app)
        resp = client.get("/widget-metrics")
        assert resp.status_code == 200
        data = resp.json()
        assert data["bssid_count"] == 1
        assert data["handshake_count"] == 5
        assert data["rx_kbps"] == 1.0
        assert data["tx_kbps"] == 2.0
        assert data["battery_percent"] == 75.0
        assert data["battery_plugged"] is True
        assert data["vehicle_speed"] == 30.0
        assert data["vehicle_rpm"] == 1500.0
        assert data["engine_load"] == 50.0


def test_logs_endpoint_returns_lines_async() -> None:
    async def fake_tail(_path: str, _lines: int) -> list[str]:
        return ["a", "b"]

    with (
        mock.patch("service.async_tail_file", fake_tail),
        mock.patch("piwardrive.service.async_tail_file", fake_tail),
    ):
        client = TestClient(service.app)
        resp = client.get("/logs?lines=2")
        assert resp.status_code == 200
        assert resp.json()["lines"] == ["a", "b"]


def test_logs_endpoint_handles_sync_function() -> None:
    def fake_tail(_path: str, _lines: int) -> list[str]:
        return ["x", "y"]

    with (
        mock.patch("service.async_tail_file", fake_tail),
        mock.patch("piwardrive.service.async_tail_file", fake_tail),
    ):
        client = TestClient(service.app)
        resp = client.get("/logs?lines=2")
        assert resp.status_code == 200
        assert resp.json()["lines"] == ["x", "y"]


def test_logs_endpoint_allows_whitelisted_path() -> None:
    async def fake_tail(path: str, _lines: int) -> list[str]:
        return [path]

    allowed = service.ALLOWED_LOG_PATHS[0]
    with (
        mock.patch("service.async_tail_file", fake_tail),
        mock.patch("piwardrive.service.async_tail_file", fake_tail),
    ):
        client = TestClient(service.app)
        resp = client.get(f"/logs?path={allowed}")
        assert resp.status_code == 200
        assert resp.json()["lines"] == [allowed]


def test_logs_endpoint_rejects_unknown_path() -> None:
    called = False

    async def fake_tail(_p: str, _l: int) -> list[str]:
        nonlocal called
        called = True
        return []

    with (
        mock.patch("service.async_tail_file", fake_tail),
        mock.patch("piwardrive.service.async_tail_file", fake_tail),
    ):
        client = TestClient(service.app)
        resp = client.get("/logs?path=/not/allowed.log")
        assert resp.status_code == 400
        assert not called


def test_command_endpoint_runs_command() -> None:
    class DummyProc:
        async def communicate(self) -> tuple[bytes, bytes]:
            return b"out", b""

        def kill(self) -> None:
            pass

    async def fake_create(cmd: str, **_k: Any) -> DummyProc:
        assert cmd == "echo hi"
        return DummyProc()

    with (
        mock.patch("service.asyncio.create_subprocess_shell", fake_create),
        mock.patch("piwardrive.service.asyncio.create_subprocess_shell", fake_create),
    ):
        client = TestClient(service.app)
        resp = client.post("/command", json={"cmd": "echo hi"})
        assert resp.status_code == 200
        assert resp.json()["output"] == "out"


def test_command_endpoint_requires_cmd() -> None:
    client = TestClient(service.app)
    resp = client.post("/command", json={})
    assert resp.status_code == 400


def test_websocket_status_stream() -> None:
    rec = persistence.HealthRecord(
        timestamp="t",
        cpu_temp=1.0,
        cpu_percent=2.0,
        memory_percent=3.0,
        disk_percent=4.0,
    )

    async def fake_load(_: int = 5) -> list:
        return [rec]

    async def fake_fetch() -> tuple[list, list, int]:
        return ([{"signal_dbm": -10}], [], 5)

    with (
        mock.patch("service.load_recent_health", fake_load),
        mock.patch("piwardrive.service.load_recent_health", fake_load),
        mock.patch("service.fetch_metrics_async", fake_fetch),
        mock.patch("piwardrive.service.fetch_metrics_async", fake_fetch),
        mock.patch("service.get_cpu_temp", return_value=40.0),
        mock.patch("piwardrive.service.get_cpu_temp", return_value=40.0),
        mock.patch("service.get_network_throughput", return_value=(1.0, 2.0)),
        mock.patch(
            "piwardrive.service.get_network_throughput", return_value=(1.0, 2.0)
        ),
        mock.patch("service.get_gps_fix_quality", return_value="3D"),
        mock.patch("piwardrive.service.get_gps_fix_quality", return_value="3D"),
        mock.patch("service.service_status_async", side_effect=[True, False]),
        mock.patch(
            "service.psutil.sensors_battery",
            return_value=SimpleNamespace(percent=50.0, power_plugged=False),
        ),
        mock.patch("service.vehicle_sensors.read_speed_obd", return_value=70.0),
        mock.patch("service.vehicle_sensors.read_rpm_obd", return_value=2000.0),
        mock.patch("service.vehicle_sensors.read_engine_load_obd", return_value=60.0),
    ):
        client = TestClient(service.app)
        with client.websocket_connect("/ws/status") as ws:
            data = ws.receive_json()
            assert data["status"][0]["cpu_percent"] == 2.0
            assert data["metrics"]["bssid_count"] == 1
            assert data["metrics"]["rx_kbps"] == 1.0
            assert data["metrics"]["battery_percent"] == 50.0
            assert data["metrics"]["battery_plugged"] is False
            assert data["metrics"]["vehicle_speed"] == 70.0
            assert data["metrics"]["vehicle_rpm"] == 2000.0
            assert data["metrics"]["engine_load"] == 60.0
            assert data["seq"] == 0
            assert isinstance(data["timestamp"], float)
            assert data["errors"] == 0


def test_sse_status_stream() -> None:
    rec = persistence.HealthRecord(
        timestamp="t",
        cpu_temp=1.0,
        cpu_percent=2.0,
        memory_percent=3.0,
        disk_percent=4.0,
    )

    async def fake_load(_: int = 5) -> list:
        return [rec]

    async def fake_fetch() -> tuple[list, list, int]:
        return ([{"signal_dbm": -10}], [], 5)

    with (
        mock.patch("service.load_recent_health", fake_load),
        mock.patch("piwardrive.service.load_recent_health", fake_load),
        mock.patch("service.fetch_metrics_async", fake_fetch),
        mock.patch("piwardrive.service.fetch_metrics_async", fake_fetch),
        mock.patch("service.get_cpu_temp", return_value=40.0),
        mock.patch("piwardrive.service.get_cpu_temp", return_value=40.0),
        mock.patch("service.get_network_throughput", return_value=(1.0, 2.0)),
        mock.patch(
            "piwardrive.service.get_network_throughput", return_value=(1.0, 2.0)
        ),
        mock.patch("service.get_gps_fix_quality", return_value="3D"),
        mock.patch("piwardrive.service.get_gps_fix_quality", return_value="3D"),
        mock.patch("service.service_status_async", side_effect=[True, False]),
        mock.patch(
            "service.psutil.sensors_battery",
            return_value=SimpleNamespace(percent=50.0, power_plugged=False),
        ),
        mock.patch("service.vehicle_sensors.read_speed_obd", return_value=70.0),
        mock.patch("service.vehicle_sensors.read_rpm_obd", return_value=2000.0),
        mock.patch("service.vehicle_sensors.read_engine_load_obd", return_value=60.0),
    ):
        client = TestClient(service.app)
        with client.stream("GET", "/sse/status") as resp:
            line = next(resp.iter_lines())
            if not line:
                line = next(resp.iter_lines())
            payload = json.loads(line.split("data: ", 1)[1])
            assert payload["status"][0]["cpu_percent"] == 2.0
            assert payload["metrics"]["bssid_count"] == 1
            assert payload["metrics"]["rx_kbps"] == 1.0
            assert payload["metrics"]["battery_percent"] == 50.0
            assert payload["metrics"]["battery_plugged"] is False
            assert payload["metrics"]["vehicle_speed"] == 70.0
            assert payload["metrics"]["vehicle_rpm"] == 2000.0
            assert payload["metrics"]["engine_load"] == 60.0
            assert payload["seq"] == 0
            assert isinstance(payload["timestamp"], float)
            assert payload["errors"] == 0


def test_ws_aps_stream() -> None:
    async def fake_load(after: float | None = None) -> list:
        return [
            {
                "bssid": "aa",
                "ssid": "A",
                "encryption": "WPA2",
                "lat": 1.0,
                "lon": 2.0,
                "last_time": 1,
            }
        ]

    with (
        mock.patch("service.load_ap_cache", fake_load),
        mock.patch("piwardrive.service.load_ap_cache", fake_load),
    ):
        client = TestClient(service.app)
        with client.websocket_connect("/ws/aps") as ws:
            data = ws.receive_json()
            assert data["aps"][0]["ssid"] == "A"
            assert data["seq"] == 0
            assert "load_time" in data


def test_sse_aps_stream() -> None:
    async def fake_load(after: float | None = None) -> list:
        return [
            {
                "bssid": "bb",
                "ssid": "B",
                "encryption": "OPEN",
                "lat": 3.0,
                "lon": 4.0,
                "last_time": 2,
            }
        ]

    with (
        mock.patch("service.load_ap_cache", fake_load),
        mock.patch("piwardrive.service.load_ap_cache", fake_load),
    ):
        client = TestClient(service.app)
        with client.stream("GET", "/sse/aps") as resp:
            line = next(resp.iter_lines())
            if not line:
                line = next(resp.iter_lines())
            payload = json.loads(line.split("data: ", 1)[1])
            assert payload["aps"][0]["ssid"] == "B"
            assert payload["seq"] == 0
            assert "load_time" in payload


def test_websocket_timeout_closes_connection() -> None:
    async def fake_load(_: int = 5) -> list:
        return []

    async def fake_fetch() -> tuple[list, list, int]:
        return ([], [], 0)

    async def send_timeout(*_: any, **__: any) -> None:
        raise asyncio.TimeoutError

    with (
        mock.patch("service.load_recent_health", fake_load),
        mock.patch("piwardrive.service.load_recent_health", fake_load),
        mock.patch("service.fetch_metrics_async", fake_fetch),
        mock.patch("piwardrive.service.fetch_metrics_async", fake_fetch),
        mock.patch("service.WebSocket.send_json", side_effect=send_timeout),
        mock.patch("service.get_cpu_temp", return_value=40.0),
        mock.patch("piwardrive.service.get_cpu_temp", return_value=40.0),
        mock.patch("service.get_network_throughput", return_value=(1.0, 2.0)),
        mock.patch(
            "piwardrive.service.get_network_throughput", return_value=(1.0, 2.0)
        ),
        mock.patch("service.get_gps_fix_quality", return_value="3D"),
        mock.patch("piwardrive.service.get_gps_fix_quality", return_value="3D"),
        mock.patch("service.service_status_async", side_effect=[True, False]),
        mock.patch(
            "service.psutil.sensors_battery",
            return_value=SimpleNamespace(percent=80.0, power_plugged=True),
        ),
        mock.patch("service.vehicle_sensors.read_speed_obd", return_value=20.0),
        mock.patch("service.vehicle_sensors.read_rpm_obd", return_value=1000.0),
        mock.patch("service.vehicle_sensors.read_engine_load_obd", return_value=30.0),
    ):
        client = TestClient(service.app)
        with pytest.raises(WebSocketDisconnect):
            with client.websocket_connect("/ws/status") as ws:
                ws.receive_json()


def test_get_config_endpoint() -> None:
    with mock.patch("service.config.load_config") as load:
        load.return_value = service.config.Config(theme="Green")
        client = TestClient(service.app)
        resp = client.get("/config")
        assert resp.status_code == 200
        assert resp.json()["theme"] == "Green"


def test_update_config_endpoint_success() -> None:
    cfg = service.config.Config(theme="Dark")
    with (
        mock.patch("service.config.load_config", return_value=cfg),
        mock.patch("service.config.save_config") as save,
    ):
        client = TestClient(service.app)
        resp = client.post("/config", json={"theme": "Light"})
        assert resp.status_code == 200
        assert resp.json()["theme"] == "Light"
        args = save.call_args[0][0]
        assert args.theme == "Light"


def test_update_config_endpoint_invalid_key() -> None:
    cfg = service.config.Config()
    with mock.patch("service.config.load_config", return_value=cfg):
        client = TestClient(service.app)
        resp = client.post("/config", json={"bad": 1})
        assert resp.status_code == 400


def test_dashboard_settings_endpoints() -> None:
    settings = service.DashboardSettings(
        layout=[{"cls": "W"}],
        widgets=["W"],
    )

    async def fake_load() -> service.DashboardSettings:
        return settings

    async def fake_save(s: service.DashboardSettings) -> None:
        assert s.layout == settings.layout
        assert s.widgets == settings.widgets

    with (
        mock.patch("service.load_dashboard_settings", fake_load),
        mock.patch("service.save_dashboard_settings", fake_save),
        mock.patch("piwardrive.service.load_dashboard_settings", fake_load),
        mock.patch("piwardrive.service.save_dashboard_settings", fake_save),
    ):
        client = TestClient(service.app)
        resp = client.get("/dashboard-settings")
        assert resp.status_code == 200
        assert resp.json() == {"layout": settings.layout, "widgets": settings.widgets}
        resp = client.post(
            "/dashboard-settings",
            json={"layout": settings.layout, "widgets": settings.widgets},
        )
        assert resp.status_code == 200
        assert resp.json() == {"layout": settings.layout, "widgets": settings.widgets}


def test_widget_metrics_auth_missing_credentials(monkeypatch) -> None:
    async def fake_fetch() -> tuple[list, list, int]:
        return ([{"signal_dbm": -10}], [], 5)

    pw_hash = security.hash_password("pw")
    monkeypatch.setenv("PW_API_PASSWORD_HASH", pw_hash)

    with (
        mock.patch("service.fetch_metrics_async", fake_fetch),
        mock.patch("piwardrive.service.fetch_metrics_async", fake_fetch),
        mock.patch("service.get_cpu_temp", return_value=40.0),
        mock.patch("piwardrive.service.get_cpu_temp", return_value=40.0),
        mock.patch("service.get_network_throughput", return_value=(1.0, 2.0)),
        mock.patch(
            "piwardrive.service.get_network_throughput", return_value=(1.0, 2.0)
        ),
        mock.patch("service.get_gps_fix_quality", return_value="3D"),
        mock.patch("piwardrive.service.get_gps_fix_quality", return_value="3D"),
        mock.patch("service.service_status_async", side_effect=[True, False]),
        mock.patch(
            "piwardrive.service.service_status_async", side_effect=[True, False]
        ),
    ):
        client = TestClient(service.app)
        resp = client.get("/widget-metrics")
        assert resp.status_code == 401


def test_widget_metrics_auth_bad_password(monkeypatch) -> None:
    async def fake_fetch() -> tuple[list, list, int]:
        return ([{"signal_dbm": -10}], [], 5)

    pw_hash = security.hash_password("pw")
    monkeypatch.setenv("PW_API_PASSWORD_HASH", pw_hash)

    with (
        mock.patch("service.fetch_metrics_async", fake_fetch),
        mock.patch("piwardrive.service.fetch_metrics_async", fake_fetch),
        mock.patch("service.get_cpu_temp", return_value=40.0),
        mock.patch("piwardrive.service.get_cpu_temp", return_value=40.0),
        mock.patch("service.get_network_throughput", return_value=(1.0, 2.0)),
        mock.patch(
            "piwardrive.service.get_network_throughput", return_value=(1.0, 2.0)
        ),
        mock.patch("service.get_gps_fix_quality", return_value="3D"),
        mock.patch("piwardrive.service.get_gps_fix_quality", return_value="3D"),
        mock.patch("service.service_status_async", side_effect=[True, False]),
        mock.patch(
            "piwardrive.service.service_status_async", side_effect=[True, False]
        ),
    ):
        client = TestClient(service.app)
        resp = client.get("/widget-metrics", auth=("u", "wrong"))
        assert resp.status_code == 401


def test_cpu_endpoint() -> None:
    with (
        mock.patch("service.get_cpu_temp", return_value=50.0),
        mock.patch("piwardrive.service.get_cpu_temp", return_value=50.0),
        mock.patch("service.psutil.cpu_percent", return_value=25.0),
        mock.patch("piwardrive.service.psutil.cpu_percent", return_value=25.0),
    ):
        client = TestClient(service.app)
        resp = client.get("/cpu")
        assert resp.status_code == 200
        assert resp.json() == {"temp": 50.0, "percent": 25.0}


def test_ram_endpoint() -> None:
    with (
        mock.patch("service.get_mem_usage", return_value=60.0),
        mock.patch("piwardrive.service.get_mem_usage", return_value=60.0),
    ):
        client = TestClient(service.app)
        resp = client.get("/ram")
        assert resp.status_code == 200
        assert resp.json() == {"percent": 60.0}


def test_storage_endpoint() -> None:
    with (
        mock.patch("service.get_disk_usage", return_value=70.0),
        mock.patch("piwardrive.service.get_disk_usage", return_value=70.0),
    ):
        client = TestClient(service.app)
        resp = client.get("/storage")
        assert resp.status_code == 200
        assert resp.json() == {"percent": 70.0}


def test_orientation_endpoint_dbus(monkeypatch) -> None:
    with (
        mock.patch(
            "service.orientation_sensors.get_orientation_dbus",
            return_value="right-up",
        ),
        mock.patch(
            "piwardrive.service.orientation_sensors.get_orientation_dbus",
            return_value="right-up",
        ),
        mock.patch(
            "service.orientation_sensors.orientation_to_angle",
            return_value=90.0,
        ),
        mock.patch(
            "piwardrive.service.orientation_sensors.orientation_to_angle",
            return_value=90.0,
        ),
        mock.patch(
            "service.orientation_sensors.read_mpu6050",
            return_value=None,
        ),
        mock.patch(
            "piwardrive.service.orientation_sensors.read_mpu6050",
            return_value=None,
        ),
    ):
        client = TestClient(service.app)
        resp = client.get("/orientation")
        assert resp.status_code == 200
        data = resp.json()
        assert data["orientation"] == "right-up"
        assert data["angle"] == 90.0
        assert data["accelerometer"] is None


def test_orientation_endpoint_mpu(monkeypatch) -> None:
    with (
        mock.patch(
            "service.orientation_sensors.get_orientation_dbus",
            return_value=None,
        ),
        mock.patch(
            "piwardrive.service.orientation_sensors.get_orientation_dbus",
            return_value=None,
        ),
        mock.patch(
            "service.orientation_sensors.read_mpu6050",
            return_value={"accelerometer": {"x": 1}, "gyroscope": {"y": 2}},
        ),
        mock.patch(
            "piwardrive.service.orientation_sensors.read_mpu6050",
            return_value={"accelerometer": {"x": 1}, "gyroscope": {"y": 2}},
        ),
    ):
        client = TestClient(service.app)
        resp = client.get("/orientation")
        assert resp.status_code == 200
        data = resp.json()
        assert data["orientation"] is None
        assert data["accelerometer"] == {"x": 1}
        assert data["gyroscope"] == {"y": 2}


def test_vehicle_endpoint(monkeypatch) -> None:
    with (
        mock.patch("service.vehicle_sensors.read_speed_obd", return_value=55.0),
        mock.patch(
            "piwardrive.service.vehicle_sensors.read_speed_obd", return_value=55.0
        ),
        mock.patch("service.vehicle_sensors.read_rpm_obd", return_value=1800.0),
        mock.patch(
            "piwardrive.service.vehicle_sensors.read_rpm_obd", return_value=1800.0
        ),
        mock.patch("service.vehicle_sensors.read_engine_load_obd", return_value=40.0),
        mock.patch(
            "piwardrive.service.vehicle_sensors.read_engine_load_obd",
            return_value=40.0,
        ),
    ):
        client = TestClient(service.app)
        resp = client.get("/vehicle")
        assert resp.status_code == 200
        assert resp.json() == {
            "speed": 55.0,
            "rpm": 1800.0,
            "engine_load": 40.0,
        }


def test_gps_endpoint(monkeypatch) -> None:
    with (
        mock.patch("service.gps_client.get_position", return_value=(1.0, 2.0)),
        mock.patch(
            "piwardrive.service.gps_client.get_position", return_value=(1.0, 2.0)
        ),
        mock.patch("service.get_gps_accuracy", return_value=5.0),
        mock.patch("piwardrive.service.get_gps_accuracy", return_value=5.0),
        mock.patch("service.get_gps_fix_quality", return_value="3D"),
        mock.patch("piwardrive.service.get_gps_fix_quality", return_value="3D"),
    ):
        client = TestClient(service.app)
        resp = client.get("/gps")
        assert resp.status_code == 200
        data = resp.json()
        assert data["lat"] == 1.0
        assert data["lon"] == 2.0
        assert data["accuracy"] == 5.0
        assert data["fix"] == "3D"


def test_service_control_endpoint_success() -> None:
    with (
        mock.patch("service.run_service_cmd", return_value=(True, "", "")),
        mock.patch("piwardrive.service.run_service_cmd", return_value=(True, "", "")),
    ):
        client = TestClient(service.app)
        resp = client.post("/service/kismet/start")
        assert resp.status_code == 200
        assert resp.json()["success"] is True


def test_service_control_endpoint_failure() -> None:
    with (
        mock.patch("service.run_service_cmd", return_value=(False, "", "boom")),
        mock.patch(
            "piwardrive.service.run_service_cmd", return_value=(False, "", "boom")
        ),
    ):
        client = TestClient(service.app)
        resp = client.post("/service/kismet/start")
        assert resp.status_code == 500


def test_service_control_endpoint_invalid_action() -> None:
    client = TestClient(service.app)
    resp = client.post("/service/kismet/invalid")
    assert resp.status_code == 400


def test_service_status_endpoint() -> None:
    with (
        mock.patch("service.service_status_async", return_value=True),
        mock.patch("piwardrive.service.service_status_async", return_value=True),
    ):
        client = TestClient(service.app)
        resp = client.get("/service/kismet")
        assert resp.status_code == 200
        assert resp.json() == {"service": "kismet", "active": True}


def test_service_status_endpoint_inactive() -> None:
    with (
        mock.patch("service.service_status_async", return_value=False),
        mock.patch("piwardrive.service.service_status_async", return_value=False),
    ):
        client = TestClient(service.app)
        resp = client.get("/service/bettercap")
        assert resp.status_code == 200
        assert resp.json() == {"service": "bettercap", "active": False}


def test_db_stats_endpoint(monkeypatch) -> None:
    async def fake_counts() -> dict:
        return {"ap_cache": 2}

    with (
        mock.patch("service.get_table_counts", fake_counts),
        mock.patch("piwardrive.service.get_table_counts", fake_counts),
        mock.patch("service._db_path", lambda: tempfile.gettempdir()),
        mock.patch("piwardrive.service._db_path", lambda: tempfile.gettempdir()),
        mock.patch("service.os.path.getsize", return_value=2048),
        mock.patch("piwardrive.service.os.path.getsize", return_value=2048),
    ):
        client = TestClient(service.app)
        resp = client.get("/db-stats")
        assert resp.status_code == 200
        assert resp.json() == {"size_kb": 2.0, "tables": {"ap_cache": 2}}


def test_lora_scan_endpoint(monkeypatch) -> None:
    async def fake_scan(iface: str = "l0") -> list[str]:
        assert iface == "l0"
        return ["a", "b"]

    with (
        mock.patch("service.async_scan_lora", fake_scan),
        mock.patch("piwardrive.service.async_scan_lora", fake_scan),
    ):
        client = TestClient(service.app)
        resp = client.get("/lora-scan?iface=l0")
        assert resp.status_code == 200
        assert resp.json() == {"count": 2, "lines": ["a", "b"]}
