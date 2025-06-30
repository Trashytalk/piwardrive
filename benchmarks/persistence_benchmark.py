"""Benchmark persistence layer throughput."""

import asyncio
import os
import tempfile
import time

import aiosqlite


async def bench(mode: str, count: int = 1000) -> tuple[float, float]:
    """Benchmark SQLite reads and writes using ``mode`` journal."""
    fd, path = tempfile.mkstemp()
    os.close(fd)
    try:
        async with aiosqlite.connect(path) as conn:
            await conn.execute(f"PRAGMA journal_mode={mode}")
            await conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, val TEXT)")
            await conn.commit()

            start = time.perf_counter()
            for i in range(count):
                await conn.execute("INSERT INTO t (val) VALUES (?)", (str(i),))
            await conn.commit()
            write = time.perf_counter() - start

            start = time.perf_counter()
            for i in range(count):
                cur = await conn.execute("SELECT val FROM t WHERE id = ?", (i + 1,))
                await cur.fetchone()
            read = time.perf_counter() - start
    finally:
        os.remove(path)
    return write / count, read / count


async def main(count: int = 1000) -> None:
    """Run benchmarks for common journal modes."""
    for mode in ["DELETE", "WAL"]:
        w, r = await bench(mode, count)
        print(f"{mode}: write {w*1000:.3f} ms/read {r*1000:.3f} ms")


if __name__ == "__main__":
    asyncio.run(main())
