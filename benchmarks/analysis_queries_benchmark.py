"""Benchmark analysis query execution time."""

import asyncio
import time
from piwardrive.services import analysis_queries


async def _bench(fn, runs=3):
    durations = []
    for _ in range(runs):
        start = time.perf_counter()
        await fn()
        durations.append(time.perf_counter() - start)
    avg = sum(durations) / runs
    print(f"{fn.__name__}: {avg:.3f}s avg over {runs} runs")


async def main():
    for fn in [
        analysis_queries.evil_twin_detection,
        analysis_queries.signal_strength_analysis,
        analysis_queries.network_security_analysis,
        analysis_queries.temporal_pattern_analysis,
        analysis_queries.mobile_device_detection,
    ]:
        await _bench(fn)


if __name__ == "__main__":
    asyncio.run(main())
