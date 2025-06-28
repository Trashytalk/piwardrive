import asyncio
import importlib
import os
import sys
from types import ModuleType, SimpleNamespace
from typing import Any


def load_scheduler(monkeypatch: Any):
    clk_mod = ModuleType("kivy.clock")

    class DummyClock:
        def __init__(self) -> None:
            self.callback: Any | None = None
            self.interval: float | None = None

        def schedule_interval(self, cb: Any, interval: float) -> Any:
            self.callback = cb
            self.interval = interval
            return SimpleNamespace(callback=cb)

        def unschedule(self, _ev: Any) -> None:
            pass

    clock = DummyClock()
    clk_mod.Clock = clock  # type: ignore[assignment, attr-defined]
    clk_mod.ClockEvent = object  # type: ignore[attr-defined]
    app_mod = ModuleType("kivy.app")
    app_mod.App = type("App", (), {"get_running_app": staticmethod(lambda: None)})  # type: ignore[assignment, attr-defined]
    monkeypatch.setitem(sys.modules, "kivy.clock", clk_mod)
    monkeypatch.setitem(sys.modules, "kivy.app", app_mod)
    if "scheduler" in sys.modules:
        monkeypatch.delitem(sys.modules, "scheduler")
    sched = importlib.import_module("scheduler")
    return sched, clock


def test_poll_scheduler_accepts_async_widget(monkeypatch: Any) -> None:
    sched, clock = load_scheduler(monkeypatch)

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
    assert clock.callback is not None
    clock.callback(0)
    assert "coro" in called


def test_poll_scheduler_handles_async_callback(monkeypatch: Any) -> None:
    sched, clock = load_scheduler(monkeypatch)

    called: list[str] = []

    async def job() -> None:
        called.append("job")

    def fake_run_async(coro: Any) -> None:
        called.append("run")
        asyncio.run(coro)

    monkeypatch.setattr(sched.utils, "run_async_task", fake_run_async)
    scheduler = sched.PollScheduler()
    scheduler.schedule("job", lambda dt: job(), 1)
    assert clock.callback is not None
    clock.callback(0)
    assert called == ["run", "job"]


def test_async_scheduler_runs_tasks(monkeypatch: Any) -> None:
    sched, _clock = load_scheduler(monkeypatch)
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
    assert async_calls


def test_async_scheduler_cancel_all_waits(monkeypatch: Any) -> None:
    sched, _clock = load_scheduler(monkeypatch)
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
    assert finished == ["done"]


def test_async_scheduler_cancel_all_gathers_exceptions(monkeypatch: Any) -> None:
    sched, _clock = load_scheduler(monkeypatch)
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
    assert not errors


def test_poll_scheduler_metrics(monkeypatch: Any) -> None:
    sched, clock = load_scheduler(monkeypatch)

    scheduler = sched.PollScheduler()

    def cb(_dt: float) -> None:
        pass

    scheduler.schedule("job", cb, 1.0)
    metrics = scheduler.get_metrics()
    assert "job" in metrics
    assert metrics["job"]["next_run"] > 0
    assert metrics["job"]["last_duration"] != metrics["job"]["last_duration"]  # NaN
    clock.callback(0)
    metrics = scheduler.get_metrics()
    assert metrics["job"]["last_duration"] >= 0


def test_async_scheduler_metrics(monkeypatch: Any) -> None:
    sched, _clock = load_scheduler(monkeypatch)
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
        assert "job" in metrics
        assert metrics["job"]["next_run"] > 0
        await asyncio.sleep(0)
        await scheduler.cancel_all()
        sched.utils.shutdown_async_loop()

    asyncio.run(runner())
