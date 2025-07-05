from __future__ import annotations

"""Scheduled report generation utilities."""

import os
from datetime import datetime, timedelta
from importlib import resources

from piwardrive import config, persistence
from piwardrive.scheduler import PollScheduler
from piwardrive.utils import run_async_task


def _load_template(name: str) -> str:
    with (
        resources.files("piwardrive.templates.reports")
        .joinpath(name)
        .open("r", encoding="utf-8") as fh
    ):
        return fh.read()


def _render(template: str, data: dict[str, object]) -> str:
    return template.format(**data)


async def generate_daily_summary(day: datetime) -> str:
    start = day.date().isoformat()
    end = (day.date() + timedelta(days=1)).isoformat()
    stats = await persistence.load_daily_detection_stats(start=start, end=end)
    total = sum(int(r.get("total_detections", 0)) for r in stats)
    unique = sum(int(r.get("unique_networks", 0)) for r in stats)
    suspicious = await persistence.count_suspicious_activities(start)
    tmpl = _load_template("daily_summary.md")
    return _render(
        tmpl,
        {
            "date": start,
            "total_detections": total,
            "unique_networks": unique,
            "suspicious_count": suspicious,
        },
    )


class ReportGeneratorService:
    """Generate daily reports and write them to ``reports_dir``."""

    def __init__(self, scheduler: PollScheduler, hour: int = 2) -> None:
        self._scheduler = scheduler
        self._event = "report_generator"
        scheduler.schedule(self._event, lambda _dt: run_async_task(self.run()), 86400)
        run_async_task(self.run())

    async def run(self) -> None:
        cfg = config.AppConfig.load()
        os.makedirs(cfg.reports_dir, exist_ok=True)
        day = datetime.utcnow()
        report = await generate_daily_summary(day)
        path = os.path.join(cfg.reports_dir, f"summary_{day.date().isoformat()}.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(report)


__all__ = ["ReportGeneratorService", "generate_daily_summary"]
