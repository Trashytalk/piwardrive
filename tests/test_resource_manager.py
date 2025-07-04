import asyncio
import os
from pathlib import Path

from piwardrive.resource_manager import ResourceManager


def test_file_and_db_cleanup(tmp_path):
    rm = ResourceManager()
    file_path = tmp_path / "test.txt"
    with rm.open_file(file_path, "w") as fh:
        fh.write("x")
        assert not fh.closed
    assert fh.closed

    db_path = tmp_path / "test.db"
    with rm.open_db(db_path) as conn:
        conn.execute("CREATE TABLE t(x int)")
        assert conn.in_transaction is False


def test_task_cancel():
    rm = ResourceManager()

    async def worker():
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            pass

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = loop.create_task(worker())
    rm.add_task(task)
    loop.run_until_complete(rm.cancel_all())
    assert task.cancelled() or task.done()
    loop.close()
