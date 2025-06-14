"""Utility functions for the PiWardrive GUI application."""

# pylint: disable=broad-exception-caught,unspecified-encoding,subprocess-run-check

import glob

import json
import asyncio
import logging
import os
import subprocess
import time

from collections import deque
from datetime import datetime
from typing import Any, Callable, Iterable, Sequence, TypeVar

from kivy.app import App

import psutil
import requests  # type: ignore

ERROR_PREFIX = "E"


def format_error(code: int, message: str) -> str:
    """Return standardized error string like ``[E001] message``."""
    return f"[{ERROR_PREFIX}{code:03d}] {message}"


try:
    import orjson as _json  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    try:
        import ujson as _json  # type: ignore
    except Exception:  # pragma: no cover - fallback
        _json = json  # type: ignore


def _loads(data: bytes | str) -> Any:
    """Parse JSON using the fastest available library."""
    return _json.loads(data)


def report_error(message: str) -> None:
    """Log the error and show an alert via the running app if possible.

    ``message`` should include a numeric error code prefix like ``[E001]``.
    """
    logging.error(message)
    try:
        app = App.get_running_app()
        if app and hasattr(app, "show_alert"):
            app.show_alert("Error", message)
    except Exception as exc:  # pragma: no cover - app may not be running
        logging.exception("Failed to display error alert: %s", exc)


T = TypeVar("T")


def retry_call(func: Callable[[], T], attempts: int = 3, delay: float = 0) -> T:
    """Call ``func`` repeatedly until it succeeds or attempts are exhausted."""
    last_exc: Exception | None = None
    for _ in range(attempts):
        try:
            return func()
        except Exception as exc:  # pragma: no cover - simple retry logic
            last_exc = exc
            if delay:
                time.sleep(delay)
    if last_exc is not None:
        raise last_exc
    raise RuntimeError("Unreachable")


def get_cpu_temp() -> float | None:
    """
    Read the Raspberry Pi CPU temperature from sysfs.
    Returns temperature in °C as a float, or None on failure.
    """
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_str = f.read().strip()
        return float(temp_str) / 1000.0
    except Exception:
        return None


def get_mem_usage() -> float | None:
    """
    Return system memory usage percentage.
    """
    try:
        return psutil.virtual_memory().percent
    except Exception:
        return None


def get_disk_usage(path: str = '/mnt/ssd') -> float | None:
    """
    Return disk usage percentage for given path.
    """
    try:
        return psutil.disk_usage(path).percent
    except Exception:
        return None


def get_smart_status(mount_point: str = '/mnt/ssd') -> str | None:
    """Return SMART health status for the device mounted at ``mount_point``."""
    try:
        dev = next(
            (p.device for p in psutil.disk_partitions(all=False)
             if p.mountpoint == mount_point),
            None,
        )
        if not dev:
            return None
        proc = subprocess.run(
            ['smartctl', '-H', dev],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            return None
        out = proc.stdout + proc.stderr
        return _parse_smartctl_output(out)
    except Exception:
        return None


def _parse_smartctl_output(output: str) -> str | None:
    """Map smartctl output to a simple status string."""
    for key, val in {"PASSED": "OK", "FAILED": "FAIL", "WARNING": "WARN"}.items():
        if key in output:
            return val
    return output.strip().splitlines()[-1] if output else None


def find_latest_file(directory: str, pattern: str = '*') -> str | None:
    """
    Find the latest file matching pattern under directory.
    """
    files = glob.glob(os.path.join(directory, pattern))
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def tail_file(path: str, lines: int = 50) -> list[str]:
    """
    Tail last N lines from a file.
    """
    try:
        with open(path, 'rb') as f:
            lines_deque: deque[str] = deque(maxlen=lines)
            for line in f:
                lines_deque.append(line.decode('utf-8', errors='ignore').rstrip())
        return list(lines_deque)
    except Exception:
        return []


def run_service_cmd(
    service: str, action: str, attempts: int = 1, delay: float = 0
) -> tuple[bool, str, str]:
    """Run ``sudo systemctl`` for ``service`` with optional retries."""

    from security import validate_service_name

    validate_service_name(service)
    if action not in {"start", "stop", "restart", "is-active"}:
        raise ValueError(f"Invalid action: {action}")

    cmd = ["sudo", "systemctl", action, service]

    def _call() -> subprocess.CompletedProcess[str]:
        return subprocess.run(cmd, capture_output=True, text=True)

    proc = retry_call(_call, attempts=attempts, delay=delay)
    out = getattr(proc, "stdout", "")
    err = getattr(proc, "stderr", "")
    return proc.returncode == 0, out, err


def service_status(service: str, attempts: int = 1, delay: float = 0) -> bool:
    """Return ``True`` if the ``systemd`` service is active."""
    try:
        ok, out, _err = run_service_cmd(
            service, "is-active", attempts=attempts, delay=delay
        )
        return ok and out.strip() == "active"
    except Exception:
        return False


def now_timestamp() -> str:
    """
    Return the current time as a formatted string.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def fetch_kismet_devices() -> tuple[list, list]:
    """
    Query Kismet REST API for devices. Returns (access_points, clients).
    Tries both /kismet/devices/all.json and /devices/all.json endpoints.
    """
    urls = [
        "http://127.0.0.1:2501/kismet/devices/all.json",
        "http://127.0.0.1:2501/devices/all.json",
    ]
    for url in urls:
        try:
            resp = requests.get(url, timeout=5)
        except requests.RequestException as exc:
            report_error(
                format_error(
                    301,
                    (
                        f"Kismet API request failed: {exc}. "
                        "Ensure Kismet is running."
                    ),
                )
            )
            continue
        try:
            if resp.status_code == 200:
                data = resp.json()
                return data.get("access_points", []), data.get("clients", [])
        except json.JSONDecodeError as exc:
            report_error(
                format_error(302, f"Kismet API JSON decode error: {exc}")
            )
        except Exception as exc:  # pragma: no cover - unexpected
            report_error(
                format_error(303, f"Kismet API error: {exc}")
            )
    return [], []


async def fetch_kismet_devices_async() -> tuple[list, list]:
    """Asynchronously fetch Kismet device data using ``asyncio``."""
    urls = [
        "http://127.0.0.1:2501/kismet/devices/all.json",
        "http://127.0.0.1:2501/devices/all.json",
    ]
    for url in urls:
        try:
            resp = await asyncio.to_thread(requests.get, url, timeout=5)
        except requests.RequestException as exc:
            report_error(
                format_error(
                    301,
                    (
                        f"Kismet API request failed: {exc}. "
                        "Ensure Kismet is running."
                    ),
                )
            )
            continue
        try:
            if resp.status_code == 200:
                data = _loads(resp.content)
                return data.get("access_points", []), data.get("clients", [])
        except Exception as exc:  # pragma: no cover - JSON parse or other
            report_error(
                format_error(303, f"Kismet API error: {exc}")
            )
    return [], []


async def fetch_metrics_async(
    log_folder: str = '/mnt/ssd/kismet_logs',
) -> tuple[list, list, int]:
    """Fetch Kismet devices and BetterCAP handshake count concurrently."""
    aps_clients = fetch_kismet_devices_async()
    handshake = asyncio.to_thread(count_bettercap_handshakes, log_folder)
    aps, clients = await aps_clients
    count = await handshake
    return aps, clients, count


def count_bettercap_handshakes(log_folder: str = '/mnt/ssd/kismet_logs') -> int:
    """
    Count .pcap handshake files in BetterCAP log directories.
    """
    pattern = os.path.join(log_folder, '*_bettercap', '*.pcap')
    return len(glob.glob(pattern))


def get_gps_accuracy() -> float | None:
    """
    Read GPS accuracy from gpspipe output (epx/epy fields).
    Returns max(epx, epy) in meters, or None on failure.
    """
    try:
        proc = subprocess.run(
            ['gpspipe', '-w', '-n', '10'],
            capture_output=True, text=True, timeout=5
        )
        for line in proc.stdout.splitlines():
            if 'epx' in line:
                rec = json.loads(line)
                epx = rec.get('epx')
                epy = rec.get('epy')
                if epx is not None and epy is not None:
                    return max(epx, epy)
    except Exception:
        pass
    return None


def get_gps_fix_quality() -> str:
    """
    Read GPS fix quality (mode) from gpspipe output.
    Returns a string like 'No Fix', '2D', '3D', or 'DGPS'.
    """
    mode_map = {1: 'No Fix', 2: '2D', 3: '3D', 4: 'DGPS'}
    try:
        proc = subprocess.run(
            ['gpspipe', '-w', '-n', '10'],
            capture_output=True, text=True, timeout=5
        )
        for line in proc.stdout.splitlines():
            if 'mode' in line:
                rec = json.loads(line)
                mode = rec.get('mode')
                return mode_map.get(mode, str(mode))
    except Exception:
        pass
    return 'Unknown'


def get_avg_rssi(aps: Iterable[dict[str, Any]]) -> float | None:
    """
    Compute average RSSI (signal_dbm) from a list of access_points.
    Returns float average or None if no data.
    """
    try:
        vals = []
        for ap in aps:
            val = ap.get('signal_dbm')
            if val is not None:
                vals.append(float(val))
        return sum(vals) / len(vals) if vals else None
    except Exception:
        return None


def parse_latest_gps_accuracy() -> float | None:
    """
    Alias for get_gps_accuracy for backward compatibility.
    """
    return get_gps_accuracy()


def tail_log_file(path: str, lines: int = 50) -> list[str]:
    """
    Alias for tail_file.
    """
    return tail_file(path, lines)


def get_recent_bssids(limit: int = 5) -> list[str]:
    """Return the most recently observed BSSIDs from the Kismet API."""
    try:
        aps, _ = fetch_kismet_devices()
        # sort by last_time (epoch) descending
        sorted_aps = sorted(aps, key=lambda ap: ap.get('last_time', 0), reverse=True)
        # extract up to `limit` BSSIDs
        return [ap.get('bssid', 'N/A') for ap in sorted_aps[:limit]]
    except Exception:
        return []


def haversine_distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Return great-circle distance between two ``(lat, lon)`` points in meters."""
    import math

    lat1, lon1 = p1
    lat2, lon2 = p2
    r = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return r * c


def polygon_area(points: Sequence[tuple[float, float]]) -> float:
    """Return planar area for a polygon of ``(lat, lon)`` points in square meters."""
    if len(points) < 3:
        return 0.0

    import math

    n = len(points)
    lat0 = sum(p[0] for p in points) / n
    lon0 = sum(p[1] for p in points) / n
    cos_lat0 = math.cos(math.radians(lat0))

    def project(p: tuple[float, float]) -> tuple[float, float]:
        return (p[1] - lon0) * cos_lat0, p[0] - lat0

    verts = [project(p) for p in points]
    prev_x, prev_y = verts[-1]
    area = 0.0
    for x, y in verts:
        area += prev_x * y - x * prev_y
        prev_x, prev_y = x, y

    area = abs(area) / 2
    meter_per_deg = 111320.0
    return area * (meter_per_deg**2)


def point_in_polygon(
    point: tuple[float, float], polygon: Sequence[tuple[float, float]]
) -> bool:
    """Return True if ``point`` is inside ``polygon`` using ray casting."""
    lat, lon = point
    inside = False
    n = len(polygon)
    if n < 3:
        return False
    for i in range(n):
        lat1, lon1 = polygon[i]
        lat2, lon2 = polygon[(i + 1) % n]
        if ((lon1 > lon) != (lon2 > lon)):
            intersect = (lat2 - lat1) * (lon - lon1) / (lon2 - lon1 + 1e-12) + lat1
            if lat < intersect:
                inside = not inside
    return inside


def load_kml(path: str) -> list[dict[str, Any]]:
    """Parse a ``.kml`` or ``.kmz`` file and return a list of features."""
    import zipfile
    import xml.etree.ElementTree as ET

    def _parse(root: ET.Element) -> list[dict[str, Any]]:
        ns = {"kml": root.tag.split("}")[0].strip("{")}
        feats = []
        for placemark in root.findall(".//kml:Placemark", ns):
            name = placemark.findtext("kml:name", default="", namespaces=ns)
            coords_text = placemark.findtext(".//kml:coordinates", namespaces=ns)
            if not coords_text:
                continue
            coords = []
            for pair in coords_text.strip().split():
                parts = pair.split(",")
                lon = float(parts[0])
                lat = float(parts[1])
                coords.append((lat, lon))
            if placemark.find("kml:Point", ns) is not None:
                feats.append({"name": name, "type": "Point", "coordinates": coords[0]})
            elif placemark.find("kml:LineString", ns) is not None:
                feats.append({
                    "name": name,
                    "type": "LineString",
                    "coordinates": coords,
                })
            elif placemark.find("kml:Polygon", ns) is not None:
                feats.append({"name": name, "type": "Polygon", "coordinates": coords})
        return feats

    if path.lower().endswith(".kmz"):
        with zipfile.ZipFile(path) as zf:
            for name in zf.namelist():
                if name.lower().endswith(".kml"):
                    data = zf.read(name)
                    root = ET.fromstring(data)
                    return _parse(root)
        return []
    root = ET.parse(path).getroot()
    return _parse(root)
