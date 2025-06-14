import numpy as np
import pandas as pd
from dataclasses import asdict
from typing import List, Dict
from persistence import HealthRecord


def compute_health_stats(records: List[HealthRecord]) -> Dict[str, float]:
    """Return average metrics for the given health ``records``."""
    if not records:
        return {}
    df = pd.DataFrame([asdict(r) for r in records])
    stats = {
        "temp_avg": float(np.nanmean(df["cpu_temp"])),
        "cpu_avg": float(df["cpu_percent"].mean()),
        "mem_avg": float(df["memory_percent"].mean()),
        "disk_avg": float(df["disk_percent"].mean()),
    }
    return stats


def plot_cpu_temp(records: List[HealthRecord], path: str) -> None:
    """Plot CPU temperature history to ``path`` using Matplotlib."""
    if not records:
        return
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    df = pd.DataFrame([asdict(r) for r in records])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.sort_values("timestamp", inplace=True)
    df["rolling"] = df["cpu_temp"].rolling(window=5, min_periods=1).mean()

    plt.figure(figsize=(4, 2))
    plt.plot(df["timestamp"], df["cpu_temp"], label="Temp")
    plt.plot(df["timestamp"], df["rolling"], label="Avg")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
