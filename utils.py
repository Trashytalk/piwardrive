"""Utility functions for the PiWardrive GUI application."""

# pylint: disable=broad-exception-caught,unspecified-encoding,subprocess-run-check

import glob

import json
import asyncio
from contextlib import asynccontextmanager
import logging
import os
import subprocess
from gpsd_client import client as gps_client
import time
import threading
import mmap

from datetime import datetime
from typing import Any, Callable, Coroutine, Iterable, Sequence, TypeVar

from sigint_suite.models import BluetoothDevice
from concurrent.futures import Future

try:  # pragma: no cover - allow running without Kivy
    from kivy.app import App as _RealApp
except Exception:
    _RealApp = None  # type: ignore

if _RealApp is not None:
    App = _RealApp
else:
    class _AppStub:
        @staticmethod
        def get_running_app() -> None:
            return None

    App = _AppStub
from enum import IntEnum

import psutil
import requests  # type: ignore
import aiohttp
import persistence

GPSD_CACHE_SECONDS = 2.0  # cache ttl in seconds
_GPSD_CACHE: dict[str, Any] = {
    "timestamp": 0.0,
    "accuracy": None,
    "fix": "Unknown",
}

# Track previous network counters for throughput calculations
_NET_IO_CACHE: dict[str | None, dict[str, Any]] = {
    None: {
        "timestamp": time.time(),
        "counters": psutil.net_io_counters(),
    }
}

# Cache for HTTP requests issued via :func:`safe_request`
SAFE_REQUEST_CACHE_SECONDS = 10.0  # default TTL in seconds
_SAFE_REQUEST_CACHE: dict[str, tuple[float, Any]] = {}


class ErrorCode(IntEnum):
    """Enumerate application error codes."""

    INVALID_KISMET_LOG_DIR = 201
    INVALID_BETTERCAP_CAPLET = 202
    GPS_POLL_RATE_INVALID = 203
    INVALID_OFFLINE_TILE_PATH = 204
    CONFIG_SAVE_FAILED = 205
    AP_POLL_RATE_INVALID = 206
    HEALTH_POLL_INVALID = 207
    LOG_ROTATE_INVALID = 208
    LOG_ARCHIVES_INVALID = 209
    BT_POLL_RATE_INVALID = 210

    KISMET_API_REQUEST_FAILED = 301
    KISMET_API_JSON_ERROR = 302
    KISMET_API_ERROR = 303


ERROR_PREFIX = "E"


def network_scanning_disabled() -> bool:
    """Return ``True`` if scanning is globally disabled."""
    app = App.get_running_app()
    if app is not None:
        disabled = bool(getattr(app, "disable_scanning", False))
    else:
        disabled = os.getenv("PW_DISABLE_SCANNING", "0").lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
    if disabled:
        logging.debug("Network scanning disabled")
    return disabled


_async_loop: asyncio.AbstractEventLoop | None = None
_async_thread: threading.Thread | None = None


def _ensure_async_loop_running() -> None:
    """Create and start the background asyncio loop if needed."""
    global _async_loop, _async_thread

    if _async_loop is None or _async_loop.is_closed():
        _async_loop = asyncio.new_event_loop()
        _async_thread = None

    if _async_thread is None or not _async_thread.is_alive():
        assert _async_loop is not None  # for type checkers
        _async_thread = threading.Thread(target=_async_loop.run_forever, daemon=True)
        _async_thread.start()


def shutdown_async_loop(timeout: float | None = 5.0) -> None:
    """Stop the background asyncio loop and join its thread."""
    global _async_loop, _async_thread

    if _async_thread is not None and _async_thread.is_alive():
        if _async_loop is not None and _async_loop.is_running():
            _async_loop.call_soon_threadsafe(_async_loop.stop)
        _async_thread.join(timeout)

    if _async_loop is not None and not _async_loop.is_closed():
        _async_loop.close()

    _async_thread = None
    _async_loop = None


def format_error(code: int | IntEnum, message: str) -> str:
    """Return standardized error string like ``[E001] message``."""
    return f"[{ERROR_PREFIX}{int(code):03d}] {message}"


try:
    import orjson as _json  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    logging.debug("orjson not available, falling back to ujson")
    try:
        import ujson as _json  # type: ignore
    except Exception:  # pragma: no cover - fallback
        logging.debug("ujson not available, using json module")
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


def require_id(widget: Any, name: str) -> Any:
    """Return ``widget.ids[name]`` or raise with context.

    The available IDs are logged before raising ``RuntimeError`` if the lookup
    fails. The error message reminds the caller to ensure ``kv/main.kv`` is
    consistent with the code.
    """
    try:
        return widget.ids[name]
    except KeyError as exc:  # pragma: no cover - UI errors
        ids = list(widget.ids.keys())
        logging.error("ID '%s' not found; available IDs: %s", name, ids)
        raise RuntimeError(
            f"ID '{name}' not found. Ensure kv/main.kv matches. Available IDs: {ids}"
        ) from exc


def run_async_task(
    coro: Coroutine[Any, Any, T],
    callback: Callable[[T], None] | None = None,
) -> Future[T]:
    """Schedule ``coro`` on the background loop and invoke ``callback``."""

    _ensure_async_loop_running()
    assert _async_loop is not None  # for mypy
    fut: Future[T] = asyncio.run_coroutine_threadsafe(coro, _async_loop)

    if callback is not None:

        def _done(f: Future[T]) -> None:
            try:
                result = f.result()
            except Exception as exc:  # pragma: no cover - background errors
                logging.exception("Async task failed: %s", exc)
            else:
                callback(result)

        fut.add_done_callback(_done)

    return fut


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


def safe_request(
    url: str,
    *,
    attempts: int = 3,
    timeout: float = 5,
    cache_seconds: float = SAFE_REQUEST_CACHE_SECONDS,
    fallback: Callable[[], T] | None = None,
    **kwargs: Any,
) -> T | Any | None:

    """Return ``requests.get(url)`` with retries and optional fallback.

    Results are cached for ``cache_seconds`` to avoid repeated network calls.
    Passing ``cache_seconds`` as ``0`` disables caching.
    """
    now = time.time()
    if cache_seconds and url in _SAFE_REQUEST_CACHE:
        ts, cached = _SAFE_REQUEST_CACHE[url]
        if now - ts <= cache_seconds:
            return cached

    def _get() -> Any:
        return requests.get(url, timeout=timeout, **kwargs)

    try:
        resp = retry_call(_get, attempts=attempts, delay=1)
        resp.raise_for_status()
        _SAFE_REQUEST_CACHE[url] = (now, resp)
        return resp
    except Exception as exc:  # pragma: no cover - network errors
        report_error(f"Request error for {url}: {exc}")
        if fallback is not None:
            try:
                result = fallback()
                _SAFE_REQUEST_CACHE[url] = (time.time(), result)
                return result
            except Exception as exc2:  # pragma: no cover - fallback failed
                report_error(f"Fallback for {url} failed: {exc2}")
        return None


def ensure_service_running(
    service: str, *, attempts: int = 3, delay: float = 1.0
) -> bool:
    """Ensure ``service`` is active, attempting a restart if not."""

    if service_status(service):
        return True

    report_error(f"{service} service not active, attempting restart")
    ok, _out, err = run_service_cmd(service, "restart", attempts=attempts, delay=delay)
    if not ok:
        msg = err.strip() if isinstance(err, str) else err
        report_error(f"Failed to restart {service}: {msg or 'Unknown error'}")
    return ok and service_status(service)


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


def get_network_throughput(iface: str | None = None) -> tuple[float, float]:
    """Return ``(rx_kbps, tx_kbps)`` since the last call.

    If ``iface`` is provided, only counters for that interface are used.
    The first call for a given ``iface`` returns ``(0.0, 0.0)``.
    """
    try:
        if iface:
            counters = psutil.net_io_counters(pernic=True)
            cur = counters.get(iface)
            if cur is None:
                return 0.0, 0.0
        else:
            cur = psutil.net_io_counters()
    except Exception:
        return 0.0, 0.0
    now = time.time()
    cache = _NET_IO_CACHE.setdefault(iface, {"counters": cur, "timestamp": now})
    prev = cache.get("counters")
    prev_ts = cache.get("timestamp", now)
    dt = now - prev_ts if prev_ts else 0.0
    rx_kbps = tx_kbps = 0.0
    if prev is not None and dt > 0:
        rx_kbps = (cur.bytes_recv - prev.bytes_recv) / dt / 1024.0
        tx_kbps = (cur.bytes_sent - prev.bytes_sent) / dt / 1024.0
    cache["counters"] = cur
    cache["timestamp"] = now
    return rx_kbps, tx_kbps


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
        try:
            proc = subprocess.run(
                ['smartctl', '-H', dev],
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError:
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
    """Return the newest file matching ``pattern`` under ``directory``."""
    dir_path = Path(directory)
    files = list(dir_path.glob(pattern))
    if not files:
        return None
    return str(max(files, key=lambda p: p.stat().st_mtime))


def tail_file(path: str, lines: int = 50) -> list[str]:
    """Return the last ``lines`` from ``path`` efficiently using ``mmap``."""
    try:
        with open(path, "rb") as f, mmap.mmap(
            f.fileno(), 0, access=mmap.ACCESS_READ
        ) as mm:
            pos = mm.size()
            for _ in range(lines + 1):
                new_pos = mm.rfind(b"\n", 0, pos)
                if new_pos == -1:
                    pos = -1
                    break
                pos = new_pos
            start = 0 if pos < 0 else pos + 1
            text = mm[start:]
            return text.decode("utf-8", errors="ignore").splitlines()[-lines:]
    except Exception:
        return []


async def async_tail_file(path: str, lines: int = 50) -> list[str]:
    """Asynchronously return the last ``lines`` from ``path``."""
    try:
        import aiofiles  # type: ignore
    except Exception:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: tail_file(path, lines))

    try:
        async with aiofiles.open(path, "rb") as f:
            fd = f.fileno()
            try:
                with mmap.mmap(fd, 0, access=mmap.ACCESS_READ) as mm:
                    pos = mm.size()
                    for _ in range(lines + 1):
                        new_pos = mm.rfind(b"\n", 0, pos)
                        if new_pos == -1:
                            pos = -1
                            break
                        pos = new_pos
                    start = 0 if pos < 0 else pos + 1
                    data = mm[start:]
                    return data.decode("utf-8", errors="ignore").splitlines()[-lines:]
            except Exception:
                await f.seek(0)
                data = await f.read()
                return data.decode("utf-8", errors="ignore").splitlines()[-lines:]
    except Exception:
        return []


def _run_service_cmd_sync(
    service: str, action: str, attempts: int = 1, delay: float = 0
) -> tuple[bool, str, str]:
    """Execute DBus service commands synchronously as a fallback."""

    import dbus
    from security import validate_service_name

    validate_service_name(service)
    if action not in {"start", "stop", "restart", "is-active"}:
        raise ValueError(f"Invalid action: {action}")

    svc_name = f"{service}.service"

    def _call() -> tuple[bool, str, str]:
        bus = dbus.SystemBus()
        systemd = bus.get_object(
            "org.freedesktop.systemd1",
            "/org/freedesktop/systemd1",
        )
        manager = dbus.Interface(systemd, "org.freedesktop.systemd1.Manager")

        if action == "start":
            manager.StartUnit(svc_name, "replace")
            return True, "", ""
        if action == "stop":
            manager.StopUnit(svc_name, "replace")
            return True, "", ""
        if action == "restart":
            manager.RestartUnit(svc_name, "replace")
            return True, "", ""

        unit_path = manager.GetUnit(svc_name)
        unit = bus.get_object("org.freedesktop.systemd1", unit_path)
        props = dbus.Interface(unit, "org.freedesktop.DBus.Properties")
        state = props.Get("org.freedesktop.systemd1.Unit", "ActiveState")
        return True, str(state), ""

    try:
        return retry_call(_call, attempts=attempts, delay=delay)
    except Exception as exc:  # pragma: no cover - DBus failures
        return False, "", str(exc)


@asynccontextmanager
async def message_bus() -> Any:
    """Yield a connected ``dbus-fast`` ``MessageBus`` instance."""

    from dbus_fast.aio import MessageBus
    from dbus_fast import BusType

    bus = MessageBus(bus_type=BusType.SYSTEM)
    await bus.connect()
    try:
        yield bus
    finally:
        bus.disconnect()


async def _run_service_cmd_async(
    service: str, action: str, attempts: int = 1, delay: float = 0
) -> tuple[bool, str, str]:
    """Async DBus implementation using ``dbus-fast``."""

    from security import validate_service_name

    validate_service_name(service)
    if action not in {"start", "stop", "restart", "is-active"}:
        raise ValueError(f"Invalid action: {action}")

    svc_name = f"{service}.service"

    try:
        import dbus_fast.aio  # type: ignore
        import dbus_fast  # type: ignore
    except Exception:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, lambda: _run_service_cmd_sync(service, action, attempts, delay)
        )

    async def _call() -> tuple[bool, str, str]:
        async with message_bus() as bus:
            intro = await bus.introspect(
                "org.freedesktop.systemd1", "/org/freedesktop/systemd1"
            )
            obj = bus.get_proxy_object(
                "org.freedesktop.systemd1", "/org/freedesktop/systemd1", intro
            )
            manager = obj.get_interface("org.freedesktop.systemd1.Manager")

            if action == "start":
                await manager.call_start_unit(svc_name, "replace")
                return True, "", ""
            if action == "stop":
                await manager.call_stop_unit(svc_name, "replace")
                return True, "", ""
            if action == "restart":
                await manager.call_restart_unit(svc_name, "replace")
                return True, "", ""

            unit_path = await manager.call_get_unit(svc_name)
            uintro = await bus.introspect("org.freedesktop.systemd1", unit_path)
            unit = bus.get_proxy_object(
                "org.freedesktop.systemd1", unit_path, uintro
            )
            props = unit.get_interface("org.freedesktop.DBus.Properties")
            state = await props.call_get(
                "org.freedesktop.systemd1.Unit", "ActiveState"
            )
            return True, str(state), ""

    async def _retry() -> tuple[bool, str, str]:
        last_exc: Exception | None = None
        for _ in range(attempts):
            try:
                return await _call()
            except Exception as exc:
                last_exc = exc
                if delay:
                    await asyncio.sleep(delay)
        if last_exc is not None:
            raise last_exc
        raise RuntimeError("Unreachable")

    try:
        return await _retry()
    except Exception as exc:  # pragma: no cover - DBus failures
        logging.exception(
            "Service command '%s %s' failed: %s", service, action, exc
        )
        return False, "", str(exc)


def run_service_cmd(
    service: str, action: str, attempts: int = 1, delay: float = 0
) -> tuple[bool, str, str]:
    """Run ``_run_service_cmd_async`` in a synchronous context."""

    fut = run_async_task(
        _run_service_cmd_async(service, action, attempts=attempts, delay=delay)
    )
    try:
        return fut.result()
    except Exception as exc:  # pragma: no cover - background failures
        logging.exception(
            "run_service_cmd encountered an error for '%s %s': %s",
            service,
            action,
            exc,
        )
        return False, "", str(exc)


async def service_status_async(
    service: str, attempts: int = 1, delay: float = 0
) -> bool:
    """Return ``True`` if the ``systemd`` service is active."""
    try:
        ok, out, _err = await _run_service_cmd_async(
            service, "is-active", attempts=attempts, delay=delay
        )
        return ok and out.strip() == "active"
    except Exception:
        return False


def service_status(service: str, attempts: int = 1, delay: float = 0) -> bool:
    """Check a service's status using the asynchronous helper."""
    fut = run_async_task(
        service_status_async(service, attempts=attempts, delay=delay)
    )
    return fut.result()


def scan_bt_devices() -> list[BluetoothDevice]:
    """Return nearby Bluetooth devices via DBus."""
    if network_scanning_disabled():
        return []
    try:
        import dbus  # type: ignore

        bus = dbus.SystemBus()
        obj = bus.get_object("org.bluez", "/")
        manager = dbus.Interface(obj, "org.freedesktop.DBus.ObjectManager")
        objects = manager.GetManagedObjects()
    except Exception:
        return []

    devices: list[BluetoothDevice] = []
    for ifaces in objects.values():
        dev = ifaces.get("org.bluez.Device1")
        if not dev:
            continue

        addr = str(dev.get("Address", ""))
        name = str(dev.get("Name", addr))
        info: dict[str, Any] = {"address": addr, "name": name}

        coords = dev.get("GPS Coordinates") or dev.get("GPSCoordinates")
        if isinstance(coords, (str, bytes)):
            vals = str(coords).split(",", 1)
            if len(vals) == 2:
                try:
                    info["lat"] = float(vals[0])
                    info["lon"] = float(vals[1])
                except Exception:
                    pass

        devices.append(BluetoothDevice(**info))

    return devices


def now_timestamp() -> str:
    """
    Return the current time as a formatted string.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def fetch_kismet_devices() -> tuple[list, list]:
    """Synchronize Kismet device data using the async helper."""

    fut = run_async_task(fetch_kismet_devices_async())
    return fut.result()


async def fetch_kismet_devices_async() -> tuple[list, list]:
    """Asynchronously fetch Kismet device data using ``aiohttp``."""

    if network_scanning_disabled():
        return [], []

    urls = [
        "http://127.0.0.1:2501/kismet/devices/all.json",
        "http://127.0.0.1:2501/devices/all.json",
    ]
    timeout = aiohttp.ClientTimeout(total=5)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async def _fetch(url: str) -> dict | None:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        try:
                            return _loads(text)
                        except Exception as exc:  # pragma: no cover - JSON error
                            report_error(
                                format_error(
                                    ErrorCode.KISMET_API_JSON_ERROR,
                                    f"Kismet API JSON decode error: {exc}",
                                )
                            )
            except aiohttp.ClientError as exc:
                report_error(
                    format_error(
                        ErrorCode.KISMET_API_REQUEST_FAILED,
                        (
                            f"Kismet API request failed: {exc}. "
                            "Ensure Kismet is running."
                        ),
                    )
                )
            except Exception as exc:  # pragma: no cover - unexpected
                report_error(
                    format_error(
                        ErrorCode.KISMET_API_ERROR,
                        f"Kismet API error: {exc}",
                    )
                )
            return None

        results = await asyncio.gather(*(_fetch(url) for url in urls))
        for data in results:
            if data is not None:
                aps = data.get("access_points", [])
                clients = data.get("clients", [])
                try:
                    await persistence.save_ap_cache(
                        [
                            {
                                "bssid": ap.get("bssid"),
                                "ssid": ap.get("ssid"),
                                "encryption": ap.get("encryption"),
                                "lat": (ap.get("gps-info") or [None, None])[0],
                                "lon": (ap.get("gps-info") or [None, None])[1],
                                "last_time": ap.get("last_time"),
                            }
                            for ap in aps
                        ]
                    )
                except Exception:
                    logging.exception("Failed to save AP cache")
                return aps, clients

    try:
        cached = await persistence.load_ap_cache()
        if cached:
            return cached, []
    except Exception:
        pass
    return [], []


async def fetch_metrics_async(
    log_folder: str = '/mnt/ssd/kismet_logs',
) -> tuple[list, list, int]:
    """Fetch Kismet devices and BetterCAP handshake count concurrently."""
    if network_scanning_disabled():
        return [], [], 0
    aps_clients = fetch_kismet_devices_async()
    handshake = asyncio.to_thread(count_bettercap_handshakes, log_folder)
    aps, clients = await aps_clients
    count = await handshake
    return aps, clients, count


def count_bettercap_handshakes(log_folder: str = '/mnt/ssd/kismet_logs') -> int:
    """Count ``.pcap`` handshake files in BetterCAP log directories."""
    base = Path(log_folder)
    count = 0
    try:
        for entry in base.iterdir():
            if entry.is_dir() and entry.name.endswith('_bettercap'):
                try:
                    for file in entry.iterdir():
                        if file.is_file() and file.name.endswith('.pcap'):
                            count += 1
                except OSError:
                    continue
    except OSError:
        return 0
    return count


def _get_cached_gps_data(force_refresh: bool = False) -> dict[str, Any] | None:
    """Return cached GPSD data or refresh if stale."""
    if not force_refresh and _GPSD_CACHE["accuracy"] is not None:
        age = time.time() - _GPSD_CACHE["timestamp"]
        if age <= GPSD_CACHE_SECONDS:
            return _GPSD_CACHE

    try:
        accuracy = gps_client.get_accuracy()
        fix = gps_client.get_fix_quality()
    except Exception:
        return _GPSD_CACHE if _GPSD_CACHE["accuracy"] is not None else None

    if accuracy is None or fix == "Unknown":
        return _GPSD_CACHE if _GPSD_CACHE["accuracy"] is not None else None

    _GPSD_CACHE["timestamp"] = time.time()
    _GPSD_CACHE["accuracy"] = accuracy
    _GPSD_CACHE["fix"] = fix
    return _GPSD_CACHE


def get_gps_accuracy(force_refresh: bool = False) -> float | None:
    """Return GPS accuracy from cached GPSD data."""
    data = _get_cached_gps_data(force_refresh)
    if not data:
        return None
    return data.get("accuracy")


def get_gps_fix_quality(force_refresh: bool = False) -> str:
    """Return human readable GPS fix quality from cached data."""
    data = _get_cached_gps_data(force_refresh)
    if not data:
        return "Unknown"
    return str(data.get("fix", "Unknown"))


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


def parse_latest_gps_accuracy(force_refresh: bool = False) -> float | None:
    """Alias for :func:`get_gps_accuracy`."""
    return get_gps_accuracy(force_refresh=force_refresh)


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


def _haversine_distance_py(p1: tuple[float, float], p2: tuple[float, float]) -> float:
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


def _polygon_area_py(points: Sequence[tuple[float, float]]) -> float:
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


def _point_in_polygon_py(
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


try:  # pragma: no cover - optional geometry C extension for speed
    from cgeom import (
        haversine_distance as _haversine_distance_c,  # type: ignore
        polygon_area as _polygon_area_c,  # type: ignore
        point_in_polygon as _point_in_polygon_c,  # type: ignore
    )
except Exception:  # pragma: no cover - extension not built
    _haversine_distance_c = None
    _polygon_area_c = None
    _point_in_polygon_c = None

haversine_distance = _haversine_distance_c or _haversine_distance_py
polygon_area = _polygon_area_c or _polygon_area_py
point_in_polygon = _point_in_polygon_c or _point_in_polygon_py


try:  # pragma: no cover - optional C extension for speed
    from ckml import parse_coords as _parse_coords  # type: ignore
except Exception:  # pragma: no cover - fallback to Python
    _parse_coords = None


def _parse_coord_text(text: str) -> list[tuple[float, float]]:
    """Parse a KML ``coordinates`` string into ``(lat, lon)`` tuples."""
    if _parse_coords:
        return _parse_coords(text)
    coords = []
    for pair in text.strip().split():
        parts = pair.split(",")
        lon = float(parts[0])
        lat = float(parts[1])
        coords.append((lat, lon))
    return coords


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
            coords = _parse_coord_text(coords_text)
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
