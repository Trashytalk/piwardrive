import asyncio
import importlib
import sys
from types import ModuleType, SimpleNamespace
from typing import Any

import pytest


def load_scheduler(monkeypatch: Any):
    if "piwardrive.scheduler" in sys.modules:
        monkeypatch.delitem(sys.modules, "piwardrive.scheduler")
    sched = importlib.import_module("piwardrive.scheduler")
    return sched


def test_poll_scheduler_accepts_async_widget(monkeypatch: Any) -> None:
    sched = load_scheduler(monkeypatch)

    class Widget:
        update_interval = 1.0

        async def update(self) -> None:
            pass

    w = Widget()
    called = {}

    def fake_run_async(coro: Any) -> None:
        called["coro"] = coro
        asyncio.run(coro)

    monkeypatch.setattr(sched.utils, "run_async_task", fake_run_async)
    scheduler = sched.PollScheduler()
    scheduler.register_widget(w, name="w")
    asyncio.run(asyncio.sleep(0))
    asyncio.run(scheduler.cancel("w")) if hasattr(scheduler, "cancel") else None
    assert "coro" in called  # nosec B101


def test_poll_scheduler_handles_async_callback(monkeypatch: Any) -> None:
    sched = load_scheduler(monkeypatch)

    called: list[str] = []

    async def job() -> None:
        called.append("job")

    def fake_run_async(coro: Any) -> None:
        called.append("run")
        asyncio.run(coro)

    monkeypatch.setattr(sched.utils, "run_async_task", fake_run_async)
    scheduler = sched.PollScheduler()
    scheduler.schedule("job", lambda dt: job(), 0.1)
    asyncio.run(asyncio.sleep(0))
    asyncio.run(scheduler.cancel("job")) if hasattr(scheduler, "cancel") else None
    assert called == ["run", "job"]  # nosec B101


def test_async_scheduler_runs_tasks(monkeypatch: Any) -> None:
    sched = load_scheduler(monkeypatch)
    async_calls: list[str] = []

    async def update() -> None:
        async_calls.append("x")

    scheduler = sched.AsyncScheduler()
    orig_sleep = asyncio.sleep

    async def fast_sleep(_):
        await orig_sleep(0)

    monkeypatch.setattr(sched.asyncio, "sleep", fast_sleep)

    async def runner():
        scheduler.schedule("job", update, 0.1)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await scheduler.cancel_all()
        sched.utils.shutdown_async_loop()

    asyncio.run(runner())
    assert async_calls  # nosec B101


def test_async_scheduler_sleep_remaining_time(monkeypatch: Any) -> None:
    sched = load_scheduler(monkeypatch)
    sleep_calls: list[float] = []
    current_time = 0.0

    orig_sleep = asyncio.sleep

    async def fake_sleep(delay: float):
        sleep_calls.append(delay)
        nonlocal current_time
        current_time += delay
        await orig_sleep(0)

    monkeypatch.setattr(sched.asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(sched.time, "time", lambda: current_time)

    async def job() -> None:
        nonlocal current_time
        current_time += 0.15

    async def runner() -> None:
        scheduler = sched.AsyncScheduler()
        scheduler.schedule("job", job, 0.1)
        await orig_sleep(0)
        await orig_sleep(0)
        await scheduler.cancel_all()
        sched.utils.shutdown_async_loop()

    asyncio.run(runner())
    assert sleep_calls[0] == pytest.approx(0.05, rel=1e-2)  # nosec B101
    assert sleep_calls[1] == pytest.approx(0.0, abs=1e-6)  # nosec B101


def test_async_scheduler_cancel_all_waits(monkeypatch: Any) -> None:
    sched = load_scheduler(monkeypatch)
    finished: list[str] = []

    done = asyncio.Event()

    async def job() -> None:
        try:
            await done.wait()
        finally:
            finished.append("done")

    scheduler = sched.AsyncScheduler()
    orig_sleep = asyncio.sleep

    async def fast_sleep(_):
        await orig_sleep(0)

    monkeypatch.setattr(sched.asyncio, "sleep", fast_sleep)

    async def runner():
        scheduler.schedule("job", job, 0.1)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await scheduler.cancel_all()
        sched.utils.shutdown_async_loop()

    asyncio.run(runner())
    assert finished == ["done"]  # nosec B101


def test_async_scheduler_cancel_all_gathers_exceptions(monkeypatch: Any) -> None:
    sched = load_scheduler(monkeypatch)
    errors: list[Any] = []

    done = asyncio.Event()

    async def job() -> None:
        try:
            await done.wait()
        finally:
            raise RuntimeError("boom")

    scheduler = sched.AsyncScheduler()
    orig_sleep = asyncio.sleep

    async def fast_sleep(_):
        await orig_sleep(0)

    monkeypatch.setattr(sched.asyncio, "sleep", fast_sleep)

    async def runner():
        loop = asyncio.get_running_loop()
        loop.set_exception_handler(lambda _l, ctx: errors.append(ctx))
        scheduler.schedule("job", job, 0.1)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await scheduler.cancel_all()
        await asyncio.sleep(0)
        sched.utils.shutdown_async_loop()

    asyncio.run(runner())
    assert not errors  # nosec B101


def test_poll_scheduler_metrics(monkeypatch: Any) -> None:
    sched = load_scheduler(monkeypatch)

    scheduler = sched.PollScheduler()

    def cb(_dt: float) -> None:
        pass

    scheduler.schedule("job", cb, 1.0)
    metrics = scheduler.get_metrics()
    assert "job" in metrics  # nosec B101
    assert metrics["job"]["next_run"] > 0  # nosec B101
    assert (
        metrics["job"]["last_duration"] != metrics["job"]["last_duration"]
    )  # NaN  # nosec B101
    asyncio.run(asyncio.sleep(0))
    metrics = scheduler.get_metrics()
    assert metrics["job"]["last_duration"] >= 0  # nosec B101


def test_async_scheduler_metrics(monkeypatch: Any) -> None:
    sched = load_scheduler(monkeypatch)
    scheduler = sched.AsyncScheduler()

    async def cb() -> None:
        pass

    orig_sleep = asyncio.sleep

    async def fast_sleep(_):
        await orig_sleep(0)

    monkeypatch.setattr(sched.asyncio, "sleep", fast_sleep)

    async def runner():
        scheduler.schedule("job", cb, 0.1)
        await asyncio.sleep(0)
        metrics = scheduler.get_metrics()
        assert "job" in metrics  # nosec B101
        assert metrics["job"]["next_run"] > 0  # nosec B101
        await asyncio.sleep(0)
        await scheduler.cancel_all()
        sched.utils.shutdown_async_loop()

    asyncio.run(runner())


def test_scheduler_rejects_invalid_interval(monkeypatch: Any) -> None:
    sched = load_scheduler(monkeypatch)

    poll = sched.PollScheduler()
    with pytest.raises(ValueError):
        poll.schedule("job", lambda dt: None, 0)

    async_sched = sched.AsyncScheduler()
    with pytest.raises(ValueError):
        async_sched.schedule("job", lambda: None, 0)
