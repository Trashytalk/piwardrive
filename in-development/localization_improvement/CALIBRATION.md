
# 🎯 Calibration Guide for Wi-Fi AP Localization

This guide explains how to properly calibrate your localization system by tuning signal strength interpretation, noise filters, and estimator parameters using `calibration_config.json`.

---

## 🔧 Configuration File: `calibration_config.json`

This file controls every major component of the localization pipeline, including noise reduction, outlier filtering, and geolocation logic.

---

## 📐 RSSI Path-Loss Calibration

### ⚙️ Keys:
- `path_loss_reference_rssi`: RSSI value at 1 meter (e.g., `-40`)
- `path_loss_exponent`: Environmental decay rate (e.g., `2.7`)

### 📏 How to Calibrate:
1. Stand exactly 1 meter from a known AP.
2. Record multiple RSSI values from that AP.
3. Average them → set as `path_loss_reference_rssi`.

4. Move to 5m, 10m, 15m...
5. Fit your RSSI readings to the path-loss model:

\`\`\`
RSSI = A - 10 * n * log10(d)
\`\`\`

6. Solve for `n`, and update `path_loss_exponent`.

---

## 📉 Kalman Filter (GPS Smoothing)

### ⚙️ Keys:
- `kalman_enable`: true / false
- `kalman_process_variance`: Lower = smoother (e.g., `0.0001`)
- `kalman_measurement_variance`: GPS error (e.g., `0.01`)

Use when GPS jitter is high or path is clean and consistent.

---

## 🧹 Outlier Filtering (DBSCAN)

### ⚙️ Keys:
- `dbscan_eps`: Max distance for clustering (e.g., `0.0005`)
- `dbscan_min_samples`: Minimum points to form a valid group (e.g., `5`)

Reduce false AP estimates by filtering weak or sporadic signals.

---

## 📍 Localization Algorithm Controls

### 🧠 Estimator Toggles:
- `use_multilateration`
- `use_bayesian`
- `hybrid_enable_ensemble`

Use one or all based on your environment and data quality.

### ⚙️ Ensemble Weighting:
```json
"hybrid_weights": {
  "multilateration": 0.4,
  "bayesian": 0.3,
  "weighted_centroid": 0.3
}
```

Change the weights to prioritize more reliable methods.

---

## 📌 Other Keys

- `min_points_for_confidence`: APs with fewer data points will be skipped
- `map_zoom_start`: Initial zoom level of the HTML map output

---

## 🧪 Tips

- 🔄 Recalibrate often in new environments
- 🚧 Use DBSCAN when mapping in cluttered or urban areas
- 📉 Lower `kalman_process_variance` if GPS is very jumpy

---

## 📚 Need Help?

Run test datasets, use known AP positions, and validate with field walks.  
For full accuracy analysis, consider adding a `ground_truth.csv` and computing RMSE across methods.
