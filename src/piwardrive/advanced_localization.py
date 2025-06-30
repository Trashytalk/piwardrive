"""Advanced Wi-Fi access point localization helpers."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd
from scipy import signal
from sklearn.cluster import DBSCAN


@dataclass
class Config:
    """Parameters controlling localization accuracy algorithms."""

    kalman_enable: bool = True
    kalman_process_variance: float = 0.0001
    kalman_measurement_variance: float = 0.01
    dbscan_eps: float = 0.0005
    dbscan_min_samples: int = 5
    centroid_rssi_weight_power: float = 1.5
    min_points_for_confidence: int = 5


def load_config(path: str | Path) -> Config:
    """Load JSON configuration from ``path``."""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return Config(**data)


# ─────────────────────────────────────────────────────────────
# SQLite helpers


def load_kismet_data(db_path: str | Path) -> pd.DataFrame:
    """Return observation rows from a Kismet SQLite log."""
    query = """
    SELECT devices.macaddr, devices.ssid, packets.lat, packets.lon,
           packets.signal AS rssi, packets.gpstime
    FROM devices
    JOIN packets ON devices.devicekey = packets.devicekey
    WHERE devices.type = 'infrastructure'
      AND packets.lat != 0 AND packets.lon != 0;
    """
    with sqlite3.connect(str(db_path)) as conn:
        df = pd.read_sql_query(query, conn)
    return df


# ─────────────────────────────────────────────────────────────
# Filtering and weighting helpers


def _kalman_1d(series: Iterable[float], q: float, r: float) -> np.ndarray:
    """Return 1D Kalman filtered ``series`` using vectorized operations."""
    arr = np.asarray(series, dtype=float)
    if arr.size == 0:
        return arr

    # Steady-state Kalman gain for constant process/measurement variance
    P = (-q + np.sqrt(q * q + 4 * q * r)) / 2
    K = (P + q) / (P + q + r)

    # IIR filter coefficients (equivalent to recursion: x[k]=x[k-1]*(1-K)+K*y[k])
    b = [K]
    a = [1, -(1 - K)]
    zi = signal.lfilter_zi(b, a) * arr[0]
    filtered, _ = signal.lfilter(b, a, arr, zi=zi)
    return filtered


def apply_kalman_filter(df: pd.DataFrame, cfg: Config) -> pd.DataFrame:
    if not cfg.kalman_enable or df.empty:
        return df
    df = df.copy()
    df["lat"] = _kalman_1d(
        df["lat"].to_numpy(),
        cfg.kalman_process_variance,
        cfg.kalman_measurement_variance,
    )
    df["lon"] = _kalman_1d(
        df["lon"].to_numpy(),
        cfg.kalman_process_variance,
        cfg.kalman_measurement_variance,
    )
    return df


def remove_outliers(df: pd.DataFrame, cfg: Config) -> pd.DataFrame:
    if df.empty:
        return df
    coords = df[["lat", "lon"]]
    labels = DBSCAN(eps=cfg.dbscan_eps, min_samples=cfg.dbscan_min_samples).fit_predict(
        coords
    )
    return df[labels != -1]


def rssi_to_distance(rssi: float, reference: float, exponent: float) -> float:
    """Convert RSSI to meters using a log-distance path-loss model."""
    return 10 ** ((reference - rssi) / (10 * exponent))


# ─────────────────────────────────────────────────────────────
# Localization


def estimate_ap_location_centroid(
    ap_data: pd.DataFrame, cfg: Config
) -> Tuple[float, float]:
    weights = ap_data["rssi"].apply(
        lambda r: max(0.01, 1 / ((100 - r) ** cfg.centroid_rssi_weight_power))
    )
    lat = np.average(ap_data["lat"], weights=weights)
    lon = np.average(ap_data["lon"], weights=weights)
    return float(lat), float(lon)


def localize_aps(df: pd.DataFrame, cfg: Config) -> Dict[str, Tuple[float, float]]:
    def _process(ap: pd.DataFrame) -> Tuple[float, float] | None:
        ap = ap.sort_values("gpstime")
        if len(ap) < cfg.min_points_for_confidence:
            return None
        ap = apply_kalman_filter(ap, cfg)
        ap = remove_outliers(ap, cfg)
        if ap.empty:
            return None
        lat, lon = estimate_ap_location_centroid(ap, cfg)
        return lat, lon

    return (
        df.groupby("macaddr", group_keys=False)
        .apply(_process, include_groups=False)
        .dropna()
        .apply(lambda t: (float(t[0]), float(t[1])))
        .to_dict()
    )


__all__ = [
    "Config",
    "load_config",
    "load_kismet_data",
    "apply_kalman_filter",
    "remove_outliers",
    "rssi_to_distance",
    "estimate_ap_location_centroid",
    "localize_aps",
]
