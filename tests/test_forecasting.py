import numpy as np

from piwardrive.analytics.forecasting import forecast_cpu_temp
from piwardrive.persistence import HealthRecord


def test_forecast_cpu_temp_deterministic():
    recs = [HealthRecord(str(i), 40.0 + i, 0.0, 0.0, 0.0) for i in range(10)]
    np.random.seed(0)
    a = forecast_cpu_temp(recs, 3)
    np.random.seed(0)
    b = forecast_cpu_temp(recs, 3)
    assert isinstance(a, list)
    assert len(a) == 3
    assert a == b
