import numpy as np

from piwardrive.advanced_localization import _kalman_1d


def test_kalman_filter_reduces_variance() -> None:
    np.random.seed(0)
    data = np.random.normal(size=100)
    filtered = _kalman_1d(data, 0.0001, 0.01)
    assert filtered.shape == data.shape
    assert np.isclose(filtered[0], data[0])
    assert filtered.var() < data.var()
