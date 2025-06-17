# main_localization.py

import pandas as pd
import numpy as np
import sqlite3
import json
from sklearn.cluster import DBSCAN
from folium import Map, Marker
from logger import setup_logger
logger = setup_logger()

# Load configuration from JSON
with open('calibration_config.json') as config_file:
    config = json.load(config_file)

# ─────────────────────────────────────────────────────────────
# Load Kismet SQLite3 logs and extract relevant AP data


def load_kismet_data(kismet_db_path):
    conn = sqlite3.connect(kismet_db_path)
    query = (
        "SELECT devices.macaddr, devices.ssid, packets.lat, packets.lon, "
        "packets.signal, packets.gpstime\n"
        "FROM devices\n"
        "JOIN packets ON devices.devicekey = packets.devicekey\n"
        "WHERE devices.type = 'infrastructure' AND packets.lat != 0 "
        "AND packets.lon != 0;"
    )
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# ─────────────────────────────────────────────────────────────
# Apply a 1D Kalman filter to latitude and longitude to reduce GPS jitter


def apply_kalman_filter(df):
    if not config.get("kalman_enable", False):
        return df

    def kalman_1d(series, q, r):
        # q = process noise, r = measurement noise
        n = len(series)
        xhat = np.zeros(n)
        P = np.zeros(n)
        xhatminus = np.zeros(n)
        Pminus = np.zeros(n)
        K = np.zeros(n)

        xhat[0] = series.iloc[0]
        P[0] = 1.0

        for k in range(1, n):
            xhatminus[k] = xhat[k-1]
            Pminus[k] = P[k-1] + q
            K[k] = Pminus[k] / (Pminus[k] + r)
            xhat[k] = xhatminus[k] + K[k] * (series.iloc[k] - xhatminus[k])
            P[k] = (1 - K[k]) * Pminus[k]

        return pd.Series(xhat, index=series.index)

    df['lat'] = kalman_1d(
        df['lat'],
        config["kalman_process_variance"],
        config["kalman_measurement_variance"],
    )
    df['lon'] = kalman_1d(
        df['lon'],
        config["kalman_process_variance"],
        config["kalman_measurement_variance"],
    )
    return df


# ─────────────────────────────────────────────────────────────
# Remove GPS/RSSI outliers using DBSCAN clustering

def remove_outliers(df):
    coords = df[['lat', 'lon']]
    db = DBSCAN(
        eps=config["dbscan_eps"],
        min_samples=config["dbscan_min_samples"]
    ).fit(coords)
    df['cluster'] = db.labels_
    return df[df["cluster"] != -1]


# ─────────────────────────────────────────────────────────────
# Convert RSSI value to estimated distance using path-loss model


def rssi_to_distance(rssi):
    A = config["path_loss_reference_rssi"]
    n = config["path_loss_exponent"]
    return 10 ** ((A - rssi) / (10 * n))

# ─────────────────────────────────────────────────────────────
# Estimate AP location using weighted RSSI centroid method


def estimate_ap_location_centroid(ap_data):
    weight_power = config["centroid_rssi_weight_power"]
    weights = ap_data['signal'].apply(
        lambda rssi: max(0.01, 1 / ((100 - rssi) ** weight_power))
    )
    lat = np.average(ap_data['lat'], weights=weights)
    lon = np.average(ap_data['lon'], weights=weights)
    return lat, lon


# ─────────────────────────────────────────────────────────────
# Process all APs in dataset and estimate their coordinates

def localize_aps(df):
    ap_coords = {}
    map_center = [df['lat'].mean(), df['lon'].mean()]
    m = Map(location=map_center, zoom_start=config["map_zoom_start"])

    for mac in df['macaddr'].unique():
        ap_data = df[df['macaddr'] == mac]
        if len(ap_data) < config["min_points_for_confidence"]:
            continue

        ap_data = ap_data.sort_values('gpstime')
        ap_data = apply_kalman_filter(ap_data)
        ap_data = remove_outliers(ap_data)

        if len(ap_data) == 0:
            continue

        lat, lon = estimate_ap_location_centroid(ap_data)
        ap_coords[mac] = (lat, lon)
        Marker([lat, lon], popup=ap_data['ssid'].iloc[0]).add_to(m)

    m.save('output/ap_locations.html')
    return ap_coords

# ─────────────────────────────────────────────────────────────
# Load the fingerprint dataset if enabled in config


def load_fingerprint_dataset():
    if not config.get("fingerprint_enabled", False):
        return None
    fp_meta = json.load(open('fingerprints/rssi_fingerprint_index.json'))
    fp_file = f"fingerprints/{fp_meta['default_environment']}"
    return pd.read_csv(fp_file)

# ─────────────────────────────────────────────────────────────
# Main pipeline execution


def main():
    logger.info("[*] Loading Kismet data...")
    data = load_kismet_data('kismet_logs/Kismet-latest.kismet')

    logger.info("[*] Loading fingerprint dataset...")
    load_fingerprint_dataset()

    logger.info("[*] Localizing access points...")
    ap_coords = localize_aps(data)

    logger.info("\n📍 Estimated AP Coordinates:")
    for mac, coords in ap_coords.items():
        logger.info(f"{mac}: {coords}")


if __name__ == '__main__':
    main()
