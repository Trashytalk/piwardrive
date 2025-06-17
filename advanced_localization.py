"""Advanced Wi-Fi access point localization helpers."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN


@dataclass
class Config:
    kalman_enable: bool = True
    kalman_process_variance: float = 0.0001
    kalman_measurement_variance: float = 0.01
    dbscan_eps: float = 0.0005
    dbscan_min_samples: int = 5
    centroid_rssi_weight_power: float = 1.5
    min_points_for_confidence: int = 5
    map_zoom_start: int = 16


def load_config(path: str | Path) -> Config:
    """Load JSON configuration from ``path``."""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return Config(**data)


# ─────────────────────────────────────────────────────────────
# SQLite helpers


def load_kismet_data(db_path: str | Path) -> pd.DataFrame:
    """Return observation rows from a Kismet SQLite log."""
    conn = sqlite3.connect(str(db_path))
    query = """
    SELECT devices.macaddr, devices.ssid, packets.lat, packets.lon,
           packets.signal AS rssi, packets.gpstime
    FROM devices
    JOIN packets ON devices.devicekey = packets.devicekey
    WHERE devices.type = 'infrastructure'
      AND packets.lat != 0 AND packets.lon != 0;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# ─────────────────────────────────────────────────────────────
# Filtering and weighting helpers


def _kalman_1d(series: Iterable[float], q: float, r: float) -> np.ndarray:
    n = len(series)
    xhat = np.zeros(n)
    P = np.zeros(n)
    xhatminus = np.zeros(n)
    Pminus = np.zeros(n)
    K = np.zeros(n)

    xhat[0] = series[0]
    P[0] = 1.0

    for k in range(1, n):
        xhatminus[k] = xhat[k - 1]
        Pminus[k] = P[k - 1] + q
        K[k] = Pminus[k] / (Pminus[k] + r)
        xhat[k] = xhatminus[k] + K[k] * (series[k] - xhatminus[k])
        P[k] = (1 - K[k]) * Pminus[k]
    return xhat


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
    coords: Dict[str, Tuple[float, float]] = {}
    for mac in df["macaddr"].unique():
        ap = df[df["macaddr"] == mac].sort_values("gpstime")
        if len(ap) < cfg.min_points_for_confidence:
            continue
        ap = apply_kalman_filter(ap, cfg)
        ap = remove_outliers(ap, cfg)
        if ap.empty:
            continue
        lat, lon = estimate_ap_location_centroid(ap, cfg)
        coords[mac] = (lat, lon)
    return coords


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
