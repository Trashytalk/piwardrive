"""Benchmark LoRa packet parsing."""

import time
from piwardrive import lora_scanner


def generate_lines(n: int) -> list[str]:
    base = "time=2024-01-01T00:00:00Z freq=868.1 rssi=-120 snr=7.5 devaddr=ABC"
    return [base] * n


def bench(count: int = 100000) -> None:
    lines = generate_lines(count)
    start = time.perf_counter()
    lora_scanner.parse_packets(lines)
    duration = time.perf_counter() - start
    print(f"{count} lines in {duration:.3f}s ({count / duration:.1f} l/s)")


if __name__ == "__main__":
    bench()
