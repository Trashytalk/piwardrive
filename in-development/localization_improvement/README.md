
# 📡 Wi-Fi Access Point Localization Project

---

## 🧭 Purpose

> Estimate the physical location of Wi-Fi Access Points using Kismet logs, GPS coordinates, and signal strength (RSSI).

This tool is designed for:

- 🔍 Wireless infrastructure mapping  
- 🔐 Red team reconnaissance  
- 📊 Signal propagation and coverage analysis  
- 🛰️ GPS-assisted AP geolocation  

---

## 🛠 Features

| ✅ Feature                          | Description                                                                 |
|-----------------------------------|-----------------------------------------------------------------------------|
| 📥 Kismet Integration             | Parses `.kismet` logs directly (SQLite3 format)                             |
| 📈 Kalman Filtering (optional)   | Smooths GPS noise over time                                                 |
| 🧹 DBSCAN Outlier Removal        | Eliminates GPS scatter/noise                                                |
| 📶 RSSI-to-Distance Modeling     | Calibrated log-distance path-loss model                                     |
| 📍 Localization Methods          | Multilateration, Bayesian, Weighted Centroid, and Hybrid Ensemble           |
| 🗺️ HTML Map Output               | Visualizes AP estimates via folium                                          |
| 🔧 JSON Config Driven            | All parameters tuned in `calibration_config.json`                           |

---

## 📦 Directory Structure

```
Localization Project/
├── kismet_logs/                # Raw Kismet logs (.kismet)
├── output/                     # HTML map outputs
├── calibration_config.json     # Main system configuration
└── main_localization.py        # Primary localization and processing script
```

---

## ⚙️ Example Configuration

```json
{
  "kalman_enable": true,
  "kalman_process_variance": 0.0001,
  "kalman_measurement_variance": 0.01,

  "dbscan_eps": 0.0005,
  "dbscan_min_samples": 5,

  "path_loss_reference_rssi": -40,
  "path_loss_exponent": 2.7,

  "centroid_rssi_weight_power": 2,
  "min_points_for_confidence": 3,

  "map_zoom_start": 16,

  "use_multilateration": true,
  "use_bayesian": true,
  "hybrid_enable_ensemble": true,
  "hybrid_weights": {
    "multilateration": 0.4,
    "bayesian": 0.3,
    "weighted_centroid": 0.3
  }
}
```

---

## 🧪 How It Works

1. Collect `.kismet` log using **Kismet** with GPS enabled
2. Place `.kismet` file into `/kismet_logs/`
3. Configure parameters in `calibration_config.json`
4. Run `main_localization.py`
5. View results in: `output/ap_locations.html`

---

## 📥 Output

- 🌍 `ap_locations.html` — interactive GPS map of estimated AP locations
- 📜 Console output — summarized coordinates per MAC

---

## 📚 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

**Python Libraries Used**:
- `pandas`
- `numpy`
- `folium`
- `scikit-learn`
- `scipy`
- `sqlite3` (standard library)

---

## 🚀 Future-Ready Features (Optional Add-Ons)

- 📡 Directional antenna support (heading-based RSSI vectors)
- 🧠 Fingerprinting & RSSI pattern matching (disabled)
- 🌐 GIS format export (GeoJSON, KML)
- 🛰️ Real-time drone/AP mapping

---

## ✨ Credits

Crafted for high-resolution AP localization, modular signal processing, and mapping automation.  
Built for OSINT, RF analysis, and offensive/defensive wireless research.

---

> 📌 Need help calibrating RSSI → distance or tuning path-loss exponents?  
> See `CALIBRATION.md` (coming soon) or ask for a guided calibration script.
