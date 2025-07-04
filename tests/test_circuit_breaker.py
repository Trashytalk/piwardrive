import asyncio

import pytest

from piwardrive.circuit_breaker import CircuitBreaker


@pytest.mark.asyncio
async def test_circuit_breaker() -> None:
    cb = CircuitBreaker(max_failures=2, reset_timeout=0.1)

    async def fail() -> None:
        raise ValueError("boom")

    async def ok() -> str:
        return "ok"

    with pytest.raises(ValueError):
        await cb.call(fail)
    with pytest.raises(ValueError):
        await cb.call(fail)
    with pytest.raises(RuntimeError):
        await cb.call(ok)
    await asyncio.sleep(0.11)
    assert await cb.call(ok) == "ok"
