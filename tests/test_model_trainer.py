import asyncio
from types import SimpleNamespace

from piwardrive import analysis, persistence
from piwardrive.services import model_trainer


class DummyScheduler:
    def __init__(self) -> None:
        self.scheduled = []

    def schedule(self, name, cb, interval):
        self.scheduled.append((name, interval))
        cb(0)

    def cancel(self, name):
        pass


async def _fake_load(limit=500):
    return [1, 2, 3]


def test_model_trainer_runs(monkeypatch):
    dummy = SimpleNamespace(count=0)

    def fit(records):
        dummy.count = len(records)

    dummy.fit = fit
    monkeypatch.setattr(analysis, "_ANOMALY_DETECTOR", dummy, raising=False)
    monkeypatch.setattr(persistence, "load_health_history", _fake_load)
    monkeypatch.setattr(model_trainer, "run_async_task", lambda coro: asyncio.run(coro))

    sched = DummyScheduler()
    model_trainer.ModelTrainer(sched, interval=5)
    assert sched.scheduled[0][0] == "ml_trainer"
    assert dummy.count == 3
