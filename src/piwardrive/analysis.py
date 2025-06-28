"""Compute summary statistics and graphs for system health records."""

import math
from dataclasses import asdict
from statistics import fmean
from typing import Dict, List

from piwardrive.persistence import HealthRecord

try:  # optional dependency
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover - fallback when pandas missing
    pd = None


def compute_health_stats(records: List[HealthRecord]) -> Dict[str, float]:
    """Return average metrics for the given health ``records``."""
    if not records:
        return {}

    temps = [r.cpu_temp for r in records if r.cpu_temp is not None]
    cpu = [r.cpu_percent for r in records]
    mem = [r.memory_percent for r in records]
    disk = [r.disk_percent for r in records]

    stats = {
        "temp_avg": float(fmean(temps)) if temps else math.nan,
        "cpu_avg": float(fmean(cpu)),
        "mem_avg": float(fmean(mem)),
        "disk_avg": float(fmean(disk)),
    }
    return stats


def plot_cpu_temp(
    records: List[HealthRecord], path: str, backend: str = "matplotlib"
) -> None:
    """Plot CPU temperature history to ``path``.

    ``backend`` may be ``"matplotlib"`` (default) or ``"plotly"`` for a GPU
    accelerated renderer using ScatterGL.  If Plotly is not installed the
    function falls back to Matplotlib.
    """
    if not records:
        return

    if pd is not None:
        df = pd.DataFrame([asdict(r) for r in records])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.sort_values("timestamp", inplace=True)
        df["rolling"] = df["cpu_temp"].rolling(window=5, min_periods=1).mean()
        times = list(df["timestamp"])
        temps = list(df["cpu_temp"])
        rolling = list(df["rolling"])
    else:  # pragma: no cover - used without pandas
        from datetime import datetime

        recs = sorted(records, key=lambda r: datetime.fromisoformat(r.timestamp))
        times = [datetime.fromisoformat(r.timestamp) for r in recs]
        temps = [r.cpu_temp for r in recs]
        rolling = []
        for i in range(len(temps)):
            window = [t for t in temps[max(0, i - 4) : i + 1] if t is not None]
            rolling.append(fmean(window) if window else math.nan)

    if backend == "plotly" and pd is not None:
        try:
            import plotly.graph_objects as go
        except Exception:
            backend = "matplotlib"  # fallback if plotly not available
        else:
            fig = go.Figure()
            fig.add_trace(go.Scattergl(x=times, y=temps, name="Temp"))
            fig.add_trace(go.Scattergl(x=times, y=rolling, name="Avg"))
            fig.write_image(path)
            return

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.figure(figsize=(4, 2))
    plt.plot(times, temps, label="Temp")
    plt.plot(times, rolling, label="Avg")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
