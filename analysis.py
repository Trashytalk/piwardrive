
from dataclasses import asdict
from typing import List, Dict
from statistics import mean
from persistence import HealthRecord


def compute_health_stats(records: List[HealthRecord]) -> Dict[str, float]:
    """Return average metrics for the given health ``records``."""
    if not records:
        return {}

    temps = [r.cpu_temp for r in records if r.cpu_temp is not None]
    cpu = [r.cpu_percent for r in records]
    mem = [r.memory_percent for r in records]
    disk = [r.disk_percent for r in records]

    stats = {
        "temp_avg": float(mean(temps)) if temps else float("nan"),
        "cpu_avg": float(mean(cpu)),
        "mem_avg": float(mean(mem)),
        "disk_avg": float(mean(disk)),
    }
    return stats


def plot_cpu_temp(records: List[HealthRecord], path: str, backend: str = "matplotlib") -> None:
    """Plot CPU temperature history to ``path``.

    ``backend`` may be ``"matplotlib"`` (default) or ``"plotly"`` for a GPU
    accelerated renderer using ScatterGL.  If Plotly is not installed the
    function falls back to Matplotlib.
    """
    if not records:
        return
    df = pd.DataFrame([asdict(r) for r in records])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.sort_values("timestamp", inplace=True)
    df["rolling"] = df["cpu_temp"].rolling(window=5, min_periods=1).mean()

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from datetime import datetime

    data = [
        (datetime.fromisoformat(r.timestamp), r.cpu_temp)
        for r in records
    ]
    data.sort(key=lambda x: x[0])

    times = [t for t, _ in data]
    temps = [v if v is not None else float("nan") for _, v in data]

    rolling = []
    for i in range(len(temps)):
        window = [t for t in temps[max(0, i - 4) : i + 1] if not (t != t)]
        if window:
            rolling.append(mean(window))
        else:
            rolling.append(float("nan"))
    recs = sorted(records, key=lambda r: datetime.fromisoformat(r.timestamp))
    times = [datetime.fromisoformat(r.timestamp) for r in recs]
    temps = [r.cpu_temp for r in recs]

    rolling = []
    for i in range(len(temps)):
        window = [t for t in temps[max(0, i - 4) : i + 1] if t is not None and not math.isnan(t)]
        rolling.append(fmean(window) if window else math.nan)



    if backend == "plotly":
        try:
            import plotly.graph_objects as go
        except Exception:
            backend = "matplotlib"  # fallback if plotly not available
        else:
            fig = go.Figure()
            fig.add_trace(
                go.Scattergl(x=df["timestamp"], y=df["cpu_temp"], name="Temp")
            )
            fig.add_trace(
                go.Scattergl(x=df["timestamp"], y=df["rolling"], name="Avg")
            )
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
