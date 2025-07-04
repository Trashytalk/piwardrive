import asyncio

import pytest

from piwardrive.cpu_pool import run_cpu_bound


def _square(x: int) -> int:
    return x * x


@pytest.mark.asyncio
async def test_run_cpu_bound() -> None:
    result = await run_cpu_bound(_square, 5)
    assert result == 25
