import numpy as np
import pandas as pd

from piwardrive.advanced_localization import (Config, _kalman_1d,
                                              apply_kalman_filter,
                                              estimate_ap_location_centroid,
                                              localize_aps, remove_outliers,
                                              rssi_to_distance)


def test_kalman_1d_empty() -> None:
    result = _kalman_1d([], 0.0001, 0.01)
    assert isinstance(result, np.ndarray)
    assert result.size == 0


def test_kalman_1d_sample_values() -> None:
    data = [1.0, 2.0, 3.0]
    filtered = _kalman_1d(data, 0.0001, 0.01)
    expected = np.array([1.0, 1.09512492, 1.27632602])
    assert np.allclose(filtered, expected, atol=1e-6)


def test_kalman_1d_constant_series() -> None:
    data = [5.0] * 5
    filtered = _kalman_1d(data, 0.0001, 0.01)
    assert np.allclose(filtered, data)


def test_apply_kalman_filter_changes_values() -> None:
    cfg = Config()
    df = pd.DataFrame({"lat": [1.0, 2.0, 3.0], "lon": [3.0, 2.0, 1.0], "gpstime": [0, 1, 2]})
    filtered = apply_kalman_filter(df, cfg)
    assert not np.allclose(filtered["lat"], df["lat"]) or not np.allclose(filtered["lon"], df["lon"])


def test_apply_kalman_filter_noop_when_disabled() -> None:
    cfg = Config(kalman_enable=False)
    df = pd.DataFrame({"lat": [1.0, 2.0], "lon": [1.0, 2.0], "gpstime": [0, 1]})
    result = apply_kalman_filter(df, cfg)
    assert result is df


def test_remove_outliers_drops_points() -> None:
    cfg = Config()
    rows = [
        {"lat": 0.0, "lon": 0.0},
        {"lat": 0.0001, "lon": 0.0},
        {"lat": 0.0, "lon": 0.0001},
        {"lat": 0.0001, "lon": 0.0001},
        {"lat": 0.0002, "lon": 0.0002},
        {"lat": 1.0, "lon": 1.0},
    ]
    df = pd.DataFrame(rows)
    cleaned = remove_outliers(df, cfg)
    assert len(cleaned) == 5
    assert not ((cleaned["lat"] == 1.0) & (cleaned["lon"] == 1.0)).any()


def test_rssi_to_distance() -> None:
    dist = rssi_to_distance(-40, -20, 2)
    assert np.isclose(dist, 10.0)


def test_estimate_ap_location_centroid_weighted() -> None:
    cfg = Config()
    ap_data = pd.DataFrame(
        {
            "lat": [0.0, 10.0],
            "lon": [0.0, 10.0],
            "rssi": [90.0, 60.0],
        }
    )
    lat, lon = estimate_ap_location_centroid(ap_data, cfg)
    assert 0.0 <= lat <= 10.0 and 0.0 <= lon <= 10.0
    assert lat < 5.0 and lon < 5.0  # closer to strong RSSI point


def test_localize_aps_returns_dict() -> None:
    cfg = Config()
    records = []
    for i in range(5):
        records.append({
            "macaddr": "aa",
            "ssid": "s1",
            "lat": 0.0,
            "lon": 0.0,
            "rssi": 80.0,
            "gpstime": i,
        })
    for i in range(5):
        records.append({
            "macaddr": "bb",
            "ssid": "s2",
            "lat": 1.0,
            "lon": 1.0,
            "rssi": 70.0,
            "gpstime": i,
        })
    df = pd.DataFrame(records)
    result = localize_aps(df, cfg)
    assert np.allclose(result["aa"], (0.0, 0.0))
    assert np.allclose(result["bb"], (1.0, 1.0))
