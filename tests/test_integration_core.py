import asyncio
import json
import os
from aiohttp import web

from piwardrive.core import persistence as cp
from piwardrive import config
import remote_sync as rs


def setup_tmp(tmp_path):
    config.CONFIG_DIR = str(tmp_path)
    os.environ["PW_DB_PATH"] = str(tmp_path / "app.db")


def test_health_record_flow(tmp_path):
    setup_tmp(tmp_path)
    rec1 = cp.HealthRecord("t1", 1.0, 10.0, 20.0, 30.0)
    rec2 = cp.HealthRecord("t2", 2.0, 11.0, 21.0, 31.0)
    asyncio.run(cp.save_health_record(rec1))
    asyncio.run(cp.save_health_record(rec2))
    rows = asyncio.run(cp.load_recent_health(2))
    assert [r.timestamp for r in rows] == ["t2", "t1"]


def test_dashboard_settings_config(tmp_path):
    setup_tmp(tmp_path)
    settings = cp.DashboardSettings(layout=[{"cls": "A"}], widgets=["A"])
    asyncio.run(cp.save_dashboard_settings(settings))
    loaded = asyncio.run(cp.load_dashboard_settings())
    assert loaded.layout == settings.layout
    assert loaded.widgets == settings.widgets


def test_sync_new_records_real_server(tmp_path):
    setup_tmp(tmp_path)
    # create some records
    for i in range(3):
        rec = cp.HealthRecord(f"t{i}", float(i), i, i, i)
        asyncio.run(cp.save_health_record(rec))

    asyncio.run(cp.flush_health_records())

    received = []

    async def handler(request):
        data = await request.post()
        f = data.get("file")
        received.append(len(f.file.read()))
        return web.Response(text="ok")

    app = web.Application()
    app.router.add_post("/", handler)

    async def run_test():
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "localhost", 8089)
        await site.start()
        db_path = cp._db_path()
        count = await rs.sync_new_records(db_path, "http://localhost:8089/")
        await runner.cleanup()
        return count

    count = asyncio.run(run_test())
    assert count == 3
    assert received and received[0] > 0
