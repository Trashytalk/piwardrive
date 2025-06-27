"""Benchmark LoRa packet parsing."""

import cProfile
import pstats
import time

from piwardrive import lora_scanner


def generate_lines(n: int) -> list[str]:
    base = "time=2024-01-01T00:00:00Z freq=868.1 rssi=-120 snr=7.5 devaddr=ABC"
    return [base] * n


def bench(count: int = 100000, parser=lora_scanner.parse_packets) -> float:
    lines = generate_lines(count)
    start = time.perf_counter()
    parser(lines)
    duration = time.perf_counter() - start
    print(
        f"{parser.__name__}: {count} lines in {duration:.3f}s "
        f"({count / duration:.1f} l/s)"
    )
    return duration


def profile_parsers(count: int = 100000) -> None:
    lines = generate_lines(count)
    for parser in [lora_scanner.parse_packets, lora_scanner.parse_packets_pandas]:
        prof = cProfile.Profile()
        prof.enable()
        parser(lines)
        prof.disable()
        stats = pstats.Stats(prof).sort_stats("tottime")
        print(f"cProfile results for {parser.__name__}:")
        stats.print_stats(5)


if __name__ == "__main__":
    bench()
    bench(parser=lora_scanner.parse_packets_pandas)
    profile_parsers()
