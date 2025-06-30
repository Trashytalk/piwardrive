"""Module vacuum_db."""

import asyncio

try:  # allow tests to provide a lightweight persistence module
    import persistence
except Exception:  # pragma: no cover - fallback
    from piwardrive import persistence

if not hasattr(persistence, "vacuum"):

    async def _noop() -> None:
        """Fallback vacuum used in tests."""
        return

    persistence.vacuum = _noop  # type: ignore[attr-defined]


def main(argv: list[str] | None = None) -> None:
    """Run VACUUM on the PiWardrive database."""
    asyncio.run(persistence.vacuum())


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
