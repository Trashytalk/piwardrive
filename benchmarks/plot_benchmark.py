"""Visualize benchmark results from CSV files."""

import time
from pathlib import Path

import pandas as pd

from piwardrive.analysis import plot_cpu_temp
from piwardrive.persistence import HealthRecord


def generate_records(n: int = 1000) -> list[HealthRecord]:
    """Return ``n`` fake :class:`HealthRecord` instances."""
    base = pd.date_range("2024-01-01", periods=n, freq="min")
    records = []
    for i, ts in enumerate(base):
        records.append(HealthRecord(str(ts), float(40 + i % 10), 20.0, 30.0, 40.0))
    return records


def main() -> None:
    """Plot the benchmark data using both backends."""
    records = generate_records()
    for backend in ["matplotlib", "plotly"]:
        path = Path(f"benchmark_{backend}.png")
        start = time.perf_counter()
        plot_cpu_temp(records, str(path), backend=backend)
        duration = time.perf_counter() - start
        print(f"{backend}: {duration:.2f}s")
        path.unlink()


if __name__ == "__main__":
    main()
