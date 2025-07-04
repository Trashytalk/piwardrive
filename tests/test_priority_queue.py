import asyncio

import pytest

from piwardrive.task_queue import PriorityTaskQueue


@pytest.mark.asyncio
async def test_priority_order() -> None:
    q = PriorityTaskQueue(workers=1)
    results: list[int] = []

    async def make_task(val: int) -> None:
        results.append(val)

    await q.start()
    q.enqueue(lambda: make_task(1), priority=1)
    q.enqueue(lambda: make_task(0), priority=0)
    await asyncio.sleep(0.1)
    await q.stop()
    assert results == [0, 1]
