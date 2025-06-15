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
