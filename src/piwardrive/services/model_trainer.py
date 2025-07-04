from __future__ import annotations

"""Automated ML model retraining service."""

from piwardrive import analysis, persistence
from piwardrive.scheduler import PollScheduler
from piwardrive.utils import run_async_task


class ModelTrainer:
    """Periodically retrain anomaly detection models."""

    def __init__(self, scheduler: PollScheduler, interval: int = 3600) -> None:
        self._scheduler = scheduler
        self._event = "ml_trainer"
        scheduler.schedule(self._event, lambda _dt: run_async_task(self.run()), interval)
        run_async_task(self.run())

    async def run(self) -> None:
        detector = getattr(analysis, "_ANOMALY_DETECTOR", None)
        if detector is None or not hasattr(detector, "fit"):
            return
        records = await persistence.load_health_history(limit=500)
        detector.fit(records)


__all__ = ["ModelTrainer"]
