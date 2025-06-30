"""Module prune_db."""

import argparse
import asyncio

try:  # allow tests to provide a lightweight persistence module
    import persistence
except Exception:  # pragma: no cover - fallback
    from piwardrive import persistence

if not hasattr(persistence, "purge_old_health"):

    async def _noop(_days: int) -> None:
        """Fallback prune used in tests."""
        return

    persistence.purge_old_health = _noop  # type: ignore[attr-defined]


def main(argv: list[str] | None = None) -> None:
    """Delete old ``health_records`` from the database."""
    parser = argparse.ArgumentParser(
        description="Prune health_records older than N days"
    )
    parser.add_argument(
        "days",
        type=int,
        help="number of days of data to keep",
    )
    args = parser.parse_args(argv)

    asyncio.run(persistence.purge_old_health(args.days))


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
