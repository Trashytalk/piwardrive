import sys
from dataclasses import asdict
from unittest import mock

sys.path.insert(0, '.')
import service
import persistence
from fastapi.testclient import TestClient


def test_status_endpoint_returns_recent_records() -> None:
    rec = persistence.HealthRecord(
        timestamp='t',
        cpu_temp=1.0,
        cpu_percent=2.0,
        memory_percent=3.0,
        disk_percent=4.0,
    )
    async def _mock(_: int) -> list:
        return [rec]

    with mock.patch('service.load_recent_health', _mock):
        client = TestClient(service.app)
        resp = client.get('/status')
        assert resp.status_code == 200
        assert resp.json() == [asdict(rec)]


def test_widget_metrics_endpoint() -> None:
    async def fake_fetch() -> tuple[list, list, int]:
        return ([{"signal_dbm": -10}], [], 5)

    with (
        mock.patch("service.fetch_metrics_async", fake_fetch),
        mock.patch("service.get_cpu_temp", return_value=40.0),
        mock.patch("service.get_gps_fix_quality", return_value="3D"),
        mock.patch("service.service_status_async", side_effect=[True, False]),
    ):
        client = TestClient(service.app)
        resp = client.get("/widget-metrics")
        assert resp.status_code == 200
        data = resp.json()
        assert data["bssid_count"] == 1
        assert data["handshake_count"] == 5


def test_logs_endpoint_returns_lines() -> None:
    with mock.patch("service.tail_file", return_value=["a", "b"]):
        client = TestClient(service.app)
        resp = client.get("/logs?lines=2")
        assert resp.status_code == 200
        assert resp.json()["lines"] == ["a", "b"]
