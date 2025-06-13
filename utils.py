"""Utility functions for the PiWardrive GUI application."""

# pylint: disable=broad-exception-caught,unspecified-encoding,subprocess-run-check

import glob
import json
import os
import subprocess
import time
from collections import deque
from datetime import datetime

import psutil
import requests

def retry_call(func, attempts=3, delay=0):
    """Call ``func`` repeatedly until it succeeds or attempts are exhausted."""
    last_exc = None
    for _ in range(attempts):
        try:
            return func()
        except Exception as exc:  # pragma: no cover - simple retry logic
            last_exc = exc
            if delay:
                time.sleep(delay)
    if last_exc:
        raise last_exc

def get_cpu_temp():
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


def get_mem_usage():
    """
    Return system memory usage percentage.
    """
    try:
        return psutil.virtual_memory().percent
    except Exception:
        return None


def get_disk_usage(path='/mnt/ssd'):
    """
    Return disk usage percentage for given path.
    """
    try:
        return psutil.disk_usage(path).percent
    except Exception:
        return None


def find_latest_file(directory, pattern='*'):
    """
    Find the latest file matching pattern under directory.
    """
    files = glob.glob(os.path.join(directory, pattern))
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def tail_file(path, lines=50):
    """
    Tail last N lines from a file.
    """
    try:
        with open(path, 'rb') as f:
            lines_deque = deque(maxlen=lines)
            for line in f:
                lines_deque.append(line.decode('utf-8', errors='ignore').rstrip())
        return list(lines_deque)
    except Exception:
        return []


def run_service_cmd(service, action):
    """
    Run `sudo systemctl <action> <service>`, capturing output.
    Returns a tuple (success: bool, stdout: str, stderr: str).
    """
    cmd = ['sudo', 'systemctl', action, service]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode == 0, proc.stdout, proc.stderr


def service_status(service):
    """
    Return True if the given systemd service is active (running).
    """
    ok, out, err = run_service_cmd(service, 'is-active')
    return ok and out.strip() == 'active'


def now_timestamp():
    """
    Return the current time as a formatted string.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def fetch_kismet_devices():
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
            if resp.status_code == 200:
                data = resp.json()
                return data.get('access_points', []), data.get('clients', [])
        except Exception:
            pass
    return [], []


def count_bettercap_handshakes(log_folder='/mnt/ssd/kismet_logs'):
    """
    Count .pcap handshake files in BetterCAP log directories.
    """
    pattern = os.path.join(log_folder, '*_bettercap', '*.pcap')
    return len(glob.glob(pattern))


def get_gps_accuracy():
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


def get_gps_fix_quality():
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


def get_avg_rssi(aps):
    """
    Compute average RSSI (signal_dbm) from a list of access_points.
    Returns float average or None if no data.
    """
    try:
        vals = [ap.get('signal_dbm') for ap in aps if ap.get('signal_dbm') is not None]
        return sum(vals) / len(vals) if vals else None
    except Exception:
        return None


def parse_latest_gps_accuracy():
    """
    Alias for get_gps_accuracy for backward compatibility.
    """
    return get_gps_accuracy()


def tail_log_file(path, lines=50):
    """
    Alias for tail_file.
    """
    return tail_file(path, lines)


def get_recent_bssids(limit=5):
    """
    Return the most recently observed BSSIDs from the Kismet API.
    """
    try:
        aps, _ = fetch_kismet_devices()
        # sort by last_time (epoch) descending
        sorted_aps = sorted(aps, key=lambda ap: ap.get('last_time', 0), reverse=True)
        # extract up to `limit` BSSIDs
        return [ap.get('bssid', 'N/A') for ap in sorted_aps[:limit]]
    except Exception:
        return []
