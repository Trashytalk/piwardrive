from __future__ import annotations

"""Predictive analytics helpers using simple ML models."""

from typing import Iterable, List, Mapping, Tuple

import numpy as np
from sklearn.linear_model import LinearRegression

__all__ = [
    "linear_forecast",
    "predict_network_lifecycle",
    "capacity_planning_forecast",
    "failure_prediction",
    "identify_expansion_opportunities",
]


def linear_forecast(
    values: Iterable[float], steps: int
) -> Tuple[List[float], List[float]]:
    """Return predictions and 95% confidence intervals for ``values``."""
    arr = np.array(list(values), dtype=float)
    if arr.size == 0:
        return [float("nan")] * steps, [float("nan")] * steps
    x = np.arange(arr.size).reshape(-1, 1)
    model = LinearRegression().fit(x, arr)
    future_x = np.arange(arr.size, arr.size + steps).reshape(-1, 1)
    preds = model.predict(future_x)
    y_pred = model.predict(x)
    resid = arr - y_pred
    s_err = float(np.sqrt(np.sum(resid**2) / max(arr.size - 2, 1)))
    t_val = 1.96
    mean_x = float(x.mean())
    denom = float(np.sum((x.flatten() - mean_x) ** 2)) or 1.0
    ci = (
        t_val
        * s_err
        * np.sqrt(1 + 1 / arr.size + (future_x.flatten() - mean_x) ** 2 / denom)
    )
    return preds.tolist(), ci.tolist()


def predict_network_lifecycle(
    records: Iterable[Mapping[str, float]], steps: int
) -> Tuple[List[float], List[float]]:
    """Forecast network activity for lifecycle management."""
    vals = [
        r.get("total_detections")
        for r in records
        if isinstance(r.get("total_detections"), (int, float))
    ]
    return linear_forecast(vals, steps)


def capacity_planning_forecast(
    records: Iterable[Mapping[str, float]], steps: int
) -> Tuple[List[float], List[float]]:
    """Predict network capacity needs based on unique networks."""
    vals = [
        r.get("unique_networks")
        for r in records
        if isinstance(r.get("unique_networks"), (int, float))
    ]
    return linear_forecast(vals, steps)


def failure_prediction(
    records: Iterable[Mapping[str, float]], steps: int
) -> Tuple[List[float], List[float]]:
    """Predict failure probability from suspicious scores."""
    vals = [
        r.get("suspicious_score")
        for r in records
        if isinstance(r.get("suspicious_score"), (int, float))
    ]
    preds, ci = linear_forecast(vals, steps)
    prob = [float(1 / (1 + np.exp(-p))) for p in preds]
    return prob, ci


def identify_expansion_opportunities(
    records: Iterable[Mapping[str, float]],
) -> List[str]:
    """Return BSSIDs with large unique location counts suggesting expansion."""
    result = []
    for r in records:
        locs = r.get("unique_locations")
        if isinstance(locs, (int, float)) and locs > 100:
            result.append(str(r.get("bssid", "")))
    return result
