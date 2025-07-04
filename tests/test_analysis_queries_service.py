import asyncio
import importlib
from dataclasses import dataclass


def _get_service(add_dummy_module):
    add_dummy_module("httpx", ASGITransport=object, AsyncClient=object)
    add_dummy_module(
        "aiohttp",
        ClientSession=object,
        ClientTimeout=lambda *a, **k: None,
        ClientError=Exception,
    )
    utils_mod = add_dummy_module("utils")

    @dataclass
    class MetricsResult:
        aps: list
        clients: list
        handshake_count: int

    utils_mod.MetricsResult = MetricsResult

    async def _dummy_async(*_a, **_k):
        return None

    utils_mod.fetch_metrics_async = _dummy_async
    utils_mod.get_avg_rssi = lambda *_a, **_k: None
    utils_mod.get_cpu_temp = lambda *_a, **_k: None
    utils_mod.get_network_throughput = lambda *_a, **_k: (0, 0)
    utils_mod.get_gps_fix_quality = lambda *_a, **_k: None
    utils_mod.service_status_async = _dummy_async
    utils_mod.async_tail_file = _dummy_async

    add_dummy_module("sync", upload_data=lambda *_a, **_k: True)

    return importlib.import_module("service")


async def _make_request(app, path):
    from httpx import ASGITransport, AsyncClient

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get(path)
    return resp


async def _dummy_result():
    return [{"ok": True}]


def test_analysis_endpoints(monkeypatch, add_dummy_module):
    add_dummy_module("psutil")
    service = _get_service(add_dummy_module)
    # patch analysis query functions
    monkeypatch.setattr(service.analysis_queries, "evil_twin_detection", _dummy_result)
    monkeypatch.setattr(service.analysis_queries, "signal_strength_analysis", _dummy_result)
    monkeypatch.setattr(service.analysis_queries, "network_security_analysis", _dummy_result)
    monkeypatch.setattr(service.analysis_queries, "temporal_pattern_analysis", _dummy_result)
    monkeypatch.setattr(service.analysis_queries, "mobile_device_detection", _dummy_result)

    async def run_tests():
        paths = [
            "/analysis/evil-twins",
            "/analysis/signal-strength",
            "/analysis/network-security",
            "/analysis/temporal-patterns",
            "/analysis/mobile-devices",
        ]
        for path in paths:
            resp = await _make_request(service.app, path)
            assert resp.status_code == 200
            assert resp.json() == [{"ok": True}]

    asyncio.run(run_tests())

