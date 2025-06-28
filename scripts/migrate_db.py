"""Module migrate_db."""

import asyncio

from piwardrive import persistence


def main(argv: list[str] | None = None) -> None:
    """Apply pending database migrations."""
    asyncio.run(persistence.migrate())


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
