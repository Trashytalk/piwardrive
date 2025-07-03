import asyncio

from piwardrive.task_queue import BackgroundTaskQueue


async def test_background_task_queue_runs_tasks() -> None:
    queue = BackgroundTaskQueue()
    results: list[str] = []

    async def job() -> None:
        await asyncio.sleep(0)
        results.append("done")

    await queue.start()
    queue.enqueue(job)
    await queue.stop()
    assert results == ["done"]  # nosec B101


async def test_run_continuous_scan_with_queue(monkeypatch) -> None:
    from piwardrive.sigint_suite import continuous_scan as cs

    async def fake_wifi():
        return ["wifi"]

    async def fake_bt():
        return ["bt"]

    monkeypatch.setattr(cs, "async_scan_wifi", fake_wifi)
    monkeypatch.setattr(cs, "async_scan_bluetooth", fake_bt)

    results: list[cs.Result] = []
    queue = BackgroundTaskQueue()
    await queue.start()
    await cs.run_continuous_scan(
        interval=0,
        iterations=2,
        on_result=lambda r: results.append(r),
        queue=queue,
    )
    await queue.stop()
    assert len(results) == 2  # nosec B101
    assert results[0]["wifi"] == ["wifi"]  # nosec B101
