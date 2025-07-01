"""Module health_stats."""

import argparse
import asyncio
import json
import logging

try:
    from persistence import load_recent_health
except Exception:  # pragma: no cover - fall back if tests replaced module
    from piwardrive.persistence import load_recent_health

from piwardrive.analysis import compute_health_stats
from piwardrive.analytics import forecast_cpu_temp
from piwardrive.logconfig import setup_logging


async def _load_records(limit: int) -> list:
    return await load_recent_health(limit)


def main(argv: list[str] | None = None) -> None:
    """Compute averaged metrics from recent health records."""
    parser = argparse.ArgumentParser(description="Show health statistics")
    parser.add_argument(
        "--limit",
        "-n",
        type=int,
        default=10,
        help="number of records to analyze",
    )
    parser.add_argument(
        "--forecast",
        type=int,
        metavar="N",
        help="forecast CPU temp N steps ahead",
    )
    args = parser.parse_args(argv)

    setup_logging(stdout=True)
    records = asyncio.run(_load_records(args.limit))
    stats = compute_health_stats(records)
    logging.info(json.dumps(stats))

    if args.forecast:
        pred = forecast_cpu_temp(records, args.forecast)
        logging.info(json.dumps({"forecast": pred}))


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
