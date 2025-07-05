"""Forecast system health metrics using ARIMA or Prophet."""

from __future__ import annotations

from typing import Iterable, List

import numpy as np

from ..persistence import HealthRecord

__all__ = ["forecast_cpu_temp"]


def _arima_forecast(values: list[float], steps: int) -> list[float]:
    from statsmodels.tsa.arima.model import ARIMA

    arr = np.array(values, dtype=float)
    model = ARIMA(arr, order=(1, 1, 1))
    fitted = model.fit()
    forecast = fitted.forecast(steps=steps)
    return [float(x) for x in forecast]


def _prophet_forecast(values: list[float], steps: int) -> list[float]:
    import pandas as pd
    from prophet import Prophet  # type: ignore

    df = pd.DataFrame({"ds": range(len(values)), "y": values})
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=steps, freq="S")
    forecast = model.predict(future)
    return [float(x) for x in forecast["yhat"].tail(steps)]


def forecast_cpu_temp(records: Iterable[HealthRecord], steps: int) -> List[float]:
    """Predict CPU temperature for upcoming intervals.

    Parameters
    ----------
    records:
        Historical :class:`HealthRecord` samples.
    steps:
        Number of future time steps to forecast.

    Returns
    -------
    list[float]
        Predicted CPU temperatures for each step.
    """

    temps = [r.cpu_temp for r in records if r.cpu_temp is not None]
    if not temps:
        return [float("nan")] * steps

    try:
        return _prophet_forecast(temps, steps)
    except Exception:  # pragma: no cover - optional dependency
        return _arima_forecast(temps, steps)
