import importlib
import importlib.util
import sys
from dataclasses import asdict
from pathlib import Path
from types import ModuleType

from fastapi.testclient import TestClient

from piwardrive.persistence import HealthRecord


def _load_service(monkeypatch):
    aiohttp_mod = ModuleType("aiohttp")
    aiohttp_mod.ClientSession = object  # type: ignore[attr-defined]
    aiohttp_mod.ClientTimeout = lambda *a, **k: None  # type: ignore[attr-defined]
    aiohttp_mod.ClientError = Exception  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "aiohttp", aiohttp_mod)

    utils_mod = ModuleType("utils")

    async def _dummy(*a, **k):
        return None

    utils_mod.fetch_metrics_async = _dummy
    utils_mod.get_avg_rssi = lambda *a, **k: None
    utils_mod.get_cpu_temp = lambda *a, **k: None
    utils_mod.get_network_throughput = lambda *a, **k: None
    utils_mod.get_gps_fix_quality = lambda *a, **k: None
    utils_mod.service_status_async = _dummy
    utils_mod.async_tail_file = _dummy
    monkeypatch.setitem(sys.modules, "utils", utils_mod)

    spec = importlib.util.spec_from_file_location("service", Path("service.py"))
    service = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(service)  # type: ignore[attr-defined]
    sys.modules["service"] = service
    return service


def test_sync_endpoint_success(monkeypatch):
    service = _load_service(monkeypatch)
    records = [HealthRecord("t", 1.0, 2.0, 3.0, 4.0)]

    async def fake_load(limit=100):
        return records

    async def fake_upload(data):
        assert data == [asdict(r) for r in records]
        return True

    monkeypatch.setattr(service, "load_recent_health", fake_load)
    monkeypatch.setattr(service, "upload_data", fake_upload)
    monkeypatch.setattr("piwardrive.service.load_recent_health", fake_load)
    monkeypatch.setattr("piwardrive.service.upload_data", fake_upload)

    client = TestClient(service.app)
    resp = client.post("/sync?limit=1")
    assert resp.status_code == 200
    assert resp.json() == {"uploaded": 1}


def test_sync_endpoint_failure(monkeypatch):
    service = _load_service(monkeypatch)

    async def fake_load(limit=100):
        return []

    async def fake_upload(data):
        return False

    monkeypatch.setattr(service, "load_recent_health", fake_load)
    monkeypatch.setattr(service, "upload_data", fake_upload)
    monkeypatch.setattr("piwardrive.service.load_recent_health", fake_load)
    monkeypatch.setattr("piwardrive.service.upload_data", fake_upload)

    client = TestClient(service.app)
    resp = client.post("/sync")
    assert resp.status_code == 502
