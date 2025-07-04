"""Analytics utilities."""

from .clustering import cluster_positions
from .forecasting import forecast_cpu_temp
from .iot import correlate_city_services, fingerprint_iot_devices
from .predictive import (
    capacity_planning_forecast,
    failure_prediction,
    identify_expansion_opportunities,
    linear_forecast,
    predict_network_lifecycle,
)

__all__ = [
    "cluster_positions",
    "forecast_cpu_temp",
    "fingerprint_iot_devices",
    "correlate_city_services",
    "linear_forecast",
    "predict_network_lifecycle",
    "capacity_planning_forecast",
    "failure_prediction",
    "identify_expansion_opportunities",
]
