from statistics import fmean
import math
from dataclasses import asdict
from typing import List, Dict
from persistence import HealthRecord


def compute_health_stats(records: List[HealthRecord]) -> Dict[str, float]:
    """Return average metrics for the given health ``records``."""
    if not records:
        return {}
    temps = [r.cpu_temp for r in records if r.cpu_temp is not None and not math.isnan(r.cpu_temp)]
    cpu = [r.cpu_percent for r in records]
    mem = [r.memory_percent for r in records]
    disk = [r.disk_percent for r in records]
    stats = {
        "temp_avg": fmean(temps) if temps else math.nan,
        "cpu_avg": fmean(cpu),
        "mem_avg": fmean(mem),
        "disk_avg": fmean(disk),
    }
    return stats


def plot_cpu_temp(records: List[HealthRecord], path: str) -> None:
    """Plot CPU temperature history to ``path`` using Matplotlib."""
    if not records:
        return
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from datetime import datetime

    recs = sorted(records, key=lambda r: datetime.fromisoformat(r.timestamp))
    times = [datetime.fromisoformat(r.timestamp) for r in recs]
    temps = [r.cpu_temp for r in recs]

    rolling = []
    for i in range(len(temps)):
        window = [t for t in temps[max(0, i - 4) : i + 1] if t is not None and not math.isnan(t)]
        rolling.append(fmean(window) if window else math.nan)

    plt.figure(figsize=(4, 2))
    plt.plot(times, temps, label="Temp")
    plt.plot(times, rolling, label="Avg")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
