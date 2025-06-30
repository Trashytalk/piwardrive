"""Analytics utilities comparing recent data against historical baselines."""

from .baseline import analyze_health_baseline, load_baseline_health

__all__ = ["analyze_health_baseline", "load_baseline_health"]
