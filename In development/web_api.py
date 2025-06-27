import json
import sqlite3
import subprocess
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from piwardrive.security import validate_service_name

app = FastAPI()


@app.get("/api/gps")
def get_gps():
    """Return the latest GPS entry from the wardrive database."""
    # Replace with actual DB path in production
    db_path = Path("/home/pi/.config/piwardrive/db.sqlite")
    if not db_path.exists():
        return {"lat": None, "lon": None, "time": None}
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT lat, lon, time FROM gps_tracks ORDER BY time DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"lat": row[0], "lon": row[1], "time": row[2]}
    return {"lat": None, "lon": None, "time": None}


@app.get("/api/aps")
def get_aps():
    """Return saved Wi‑Fi access points as GeoJSON."""
    file = Path("/home/pi/.config/piwardrive/export/aps.geojson")
    if file.exists():
        with file.open() as f:
            return json.load(f)
    return {"type": "FeatureCollection", "features": []}


@app.get("/api/bt")
def get_bt():
    """Return Bluetooth device data as GeoJSON."""
    file = Path("/home/pi/.config/piwardrive/export/bt.geojson")
    if file.exists():
        with file.open() as f:
            return json.load(f)
    return {"type": "FeatureCollection", "features": []}


def _toggle_service(service: str, state: str) -> dict:
    """Start or stop a systemd service."""
    validate_service_name(service)
    if state == "start":
        subprocess.run(["sudo", "systemctl", "start", service], check=False)
    elif state == "stop":
        subprocess.run(["sudo", "systemctl", "stop", service], check=False)
    return {"status": "ok"}


@app.post("/api/service/{service}/toggle")
def toggle_service(service: str, state: str):
    """Toggle an arbitrary service."""
    return _toggle_service(service, state)


@app.post("/api/kismet/toggle")
def toggle_kismet(state: str):
    """Start or stop the kismet service."""
    return _toggle_service("kismet", state)


@app.post("/api/bettercap/toggle")
def toggle_bettercap(state: str):
    """Start or stop the BetterCAP service."""
    return _toggle_service("bettercap", state)


# Serve static dashboard if available
_static = Path(__file__).parent / "web_gui"
if _static.is_dir():
    app.mount("/", StaticFiles(directory=_static, html=True), name="static")
