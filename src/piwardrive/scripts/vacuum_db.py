import asyncio
import persistence


def main(argv: list[str] | None = None) -> None:
    """Run VACUUM on the PiWardrive database."""
    asyncio.run(persistence.vacuum())


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
