"""Utility functions for the PiWardrive GUI application."""

# pylint: disable=broad-exception-caught,unspecified-encoding,subprocess-run-check

from . import fastjson
import asyncio
from contextlib import asynccontextmanager
import logging
import os
import subprocess
from pathlib import Path
from piwardrive.gpsd_client import client as gps_client
import time
import threading
import mmap
import glob

from datetime import datetime
from typing import Any, Callable, Coroutine, Iterable, Sequence, TypeVar

from piwardrive.sigint_suite.models import BluetoothDevice
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
            """
            Returns None to indicate that no running application instance is available.
            """
            return None

    App = _AppStub
from enum import IntEnum

import psutil
import requests  # type: ignore
import requests_cache
import aiohttp
from piwardrive import persistence

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

_NET_IO_CACHE_LOCK = threading.Lock()
# Cache for frequently polled system metrics
MEM_USAGE_CACHE_SECONDS = 2.0
_MEM_USAGE_CACHE: dict[str, Any] = {"timestamp": 0.0, "percent": None}

DISK_USAGE_CACHE_SECONDS = 2.0
_DISK_USAGE_CACHE: dict[str, dict[str, Any]] = {}


# Cache for HTTP requests issued via :func:`safe_request`
# Default TTL in seconds and maximum cache size
SAFE_REQUEST_CACHE_SECONDS = 10.0
SAFE_REQUEST_CACHE_MAX_SIZE = 128
_SAFE_REQUEST_CACHE: dict[str, tuple[float, Any]] = {}

_SAFE_REQUEST_CACHE_LOCK = threading.Lock()

# Cache for BetterCAP handshake counts
HANDSHAKE_CACHE_SECONDS = 10.0  # default TTL in seconds
_HANDSHAKE_CACHE: dict[str, tuple[float, int]] = {}


HTTP_SESSION = requests_cache.CachedSession(expire_after=SAFE_REQUEST_CACHE_SECONDS)


def _prune_safe_request_cache(now: float) -> None:
    """
    Removes expired or excess entries from the safe request cache based on age and maximum cache size.
    """
    expired: list[str] = []
    for url, (ts, _) in list(_SAFE_REQUEST_CACHE.items()):
        if now - ts > SAFE_REQUEST_CACHE_SECONDS:
            expired.append(url)
    for url in expired:
        _SAFE_REQUEST_CACHE.pop(url, None)

    if len(_SAFE_REQUEST_CACHE) > SAFE_REQUEST_CACHE_MAX_SIZE:
        sorted_items = sorted(_SAFE_REQUEST_CACHE.items(), key=lambda it: it[1][0])
        limit = len(_SAFE_REQUEST_CACHE) - SAFE_REQUEST_CACHE_MAX_SIZE
        for url, _ in sorted_items[:limit]:
            _SAFE_REQUEST_CACHE.pop(url, None)


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
    """
    Returns True if network scanning is globally disabled via the running app's attribute or an environment variable.
    
    Checks the application's `disable_scanning` attribute if available; otherwise, inspects the `PW_DISABLE_SCANNING` environment variable.
    """
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
    """
    Initializes and starts a background asyncio event loop in a daemon thread if one is not already running.
    """
    global _async_loop, _async_thread

    if _async_loop is None or _async_loop.is_closed():
        _async_loop = asyncio.new_event_loop()
        _async_thread = None

    if _async_thread is None or not _async_thread.is_alive():
        assert _async_loop is not None  # for type checkers
        _async_thread = threading.Thread(target=_async_loop.run_forever, daemon=True)
        _async_thread.start()


def shutdown_async_loop(timeout: float | None = 5.0) -> None:
    """
    Stops the background asyncio event loop and waits for its thread to finish.
    
    Parameters:
        timeout (float | None): Maximum time in seconds to wait for the thread to join. If None, waits indefinitely.
    """
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
    """
    Format an error code and message into a standardized string.
    
    Returns:
        str: The formatted error string in the form "[E###] message".
    """
    return f"[{ERROR_PREFIX}{int(code):03d}] {message}"


def report_error(message: str) -> None:
    """
    Logs an error message and attempts to display an alert in the running application.
    
    The message should include a numeric error code prefix (e.g., "[E001]").
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
    """
    Retrieve a widget child by ID or raise a RuntimeError with available IDs listed.
    
    If the specified ID is not found in the widget's `ids` dictionary, logs the available IDs and raises a RuntimeError with a message suggesting to check the `kv/main.kv` file for consistency.
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
    """
    Schedules a coroutine to run on the background asyncio event loop and optionally invokes a callback with its result upon completion.
    
    Parameters:
        coro (Coroutine): The coroutine to execute asynchronously.
        callback (Callable[[T], None], optional): A function to call with the result of the coroutine when it completes.
    
    Returns:
        Future[T]: A Future representing the execution of the coroutine.
    """

    _ensure_async_loop_running()
    assert _async_loop is not None  # for mypy
    fut: Future[T] = asyncio.run_coroutine_threadsafe(coro, _async_loop)

    if callback is not None:

        def _done(f: Future[T]) -> None:
            """
            Handles completion of a Future by invoking the callback with the result or logging exceptions if the task failed.
            """
            try:
                result = f.result()
            except Exception as exc:  # pragma: no cover - background errors
                logging.exception("Async task failed: %s", exc)
            else:
                callback(result)

        fut.add_done_callback(_done)

    return fut


def retry_call(func: Callable[[], T], attempts: int = 3, delay: float = 0) -> T:
    """
    Calls the provided function repeatedly until it succeeds or the specified number of attempts is exhausted.
    
    Parameters:
        func (Callable[[], T]): The function to call. It should take no arguments.
        attempts (int): Maximum number of attempts to call the function. Defaults to 3.
        delay (float): Seconds to wait between attempts. Defaults to 0.
    
    Returns:
        T: The result returned by the function if successful.
    
    Raises:
        Exception: The last exception raised by the function if all attempts fail.
    """
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
    """
    Performs a cached HTTP GET request with retries and optional fallback.
    
    Attempts to retrieve the specified URL using a cached HTTP session, retrying on failure up to the specified number of attempts. Responses are cached for the given duration in seconds. If all attempts fail, an optional fallback function is called and its result is cached and returned. Returns None if both the request and fallback fail.
    
    Parameters:
        url (str): The URL to request.
        attempts (int): Number of retry attempts on failure.
        timeout (float): Timeout in seconds for each request.
        cache_seconds (float): Duration in seconds to cache the response; set to 0 to disable caching.
        fallback (Callable[[], T] | None): Optional function to call if all attempts fail.
    
    Returns:
        The HTTP response object, the result of the fallback function, or None if both fail.
    """
    now = time.time()
    _prune_safe_request_cache(now)
    if cache_seconds and url in _SAFE_REQUEST_CACHE:
        ts, cached = _SAFE_REQUEST_CACHE[url]
        if now - ts <= cache_seconds:
            return cached
    if cache_seconds:
        with _SAFE_REQUEST_CACHE_LOCK:
            entry = _SAFE_REQUEST_CACHE.get(url)
        if entry is not None:
            ts, cached = entry
            if now - ts <= cache_seconds:
                return cached

    def _get() -> Any:
        """
        Performs an HTTP GET request using the cached session with the specified URL, timeout, cache expiration, and additional parameters.
        
        Returns:
            The HTTP response object from the cached session.
        """
        return HTTP_SESSION.get(
            url,
            timeout=timeout,
            expire_after=cache_seconds or None,
            **kwargs,
        )

    try:
        resp = retry_call(_get, attempts=attempts, delay=1)
        resp.raise_for_status()
        with _SAFE_REQUEST_CACHE_LOCK:
            _SAFE_REQUEST_CACHE[url] = (now, resp)
        return resp
    except requests.Timeout as exc:
        report_error(f"Request timeout for {url}: {exc}")
    except requests.HTTPError as exc:
        status = exc.response.status_code if getattr(
            exc, "response", None) else "Unknown"
        report_error(f"HTTP {status} error for {url}: {exc}")
    except requests.RequestException as exc:
        report_error(f"Request exception for {url}: {exc}")
    except Exception as exc:  # pragma: no cover - unexpected errors
        report_error(f"Unexpected error for {url}: {exc}")
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
    """
    Ensures that the specified systemd service is running, attempting to restart it if inactive.
    
    Parameters:
        service (str): The name of the systemd service to check and manage.
    
    Returns:
        bool: True if the service is active after any restart attempts, False otherwise.
    """
    from piwardrive.security import validate_service_name

    validate_service_name(service)

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
    Returns the current Raspberry Pi CPU temperature in degrees Celsius.
    
    Returns:
        float | None: The CPU temperature in °C, or None if the temperature cannot be read.
    """
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_str = f.read().strip()
        return float(temp_str) / 1000.0
    except Exception:
        return None


def get_mem_usage() -> float | None:
    """
    Returns the current system memory usage as a percentage, using a cached value if available and recent.
    
    Returns:
        float | None: Memory usage percentage, or None if retrieval fails.
    """
    now = time.time()
    pct = _MEM_USAGE_CACHE.get("percent")
    ts = _MEM_USAGE_CACHE.get("timestamp", 0.0)
    if pct is not None and now - ts <= MEM_USAGE_CACHE_SECONDS:
        return pct
    try:
        pct = psutil.virtual_memory().percent
    except Exception:
        return pct
    _MEM_USAGE_CACHE["timestamp"] = now
    _MEM_USAGE_CACHE["percent"] = pct
    return pct


def get_disk_usage(path: str = '/mnt/ssd') -> float | None:
    """
    Returns the disk usage percentage for the specified path, using a cached value if available and recent.
    
    Parameters:
        path (str): Filesystem path to check disk usage for. Defaults to '/mnt/ssd'.
    
    Returns:
        float | None: Disk usage percentage, or None if unavailable.
    """
    now = time.time()
    cache = _DISK_USAGE_CACHE.get(path)
    if cache is not None:
        pct_cached = cache.get("percent")
        ts = cache.get("timestamp", 0.0)
        if pct_cached is not None and now - ts <= DISK_USAGE_CACHE_SECONDS:
            return pct_cached
    try:
        pct = psutil.disk_usage(path).percent
    except Exception:
        return cache.get("percent") if cache else None
    _DISK_USAGE_CACHE[path] = {"timestamp": now, "percent": pct}
    return pct


def get_network_throughput(iface: str | None = None) -> tuple[float, float]:
    """
    Return the received and transmitted network throughput in kilobits per second since the last call.
    
    If an interface name is provided, throughput is measured for that interface only; otherwise, overall system throughput is returned. The first call for a given interface returns (0.0, 0.0).
        
    Returns:
        tuple[float, float]: A tuple containing (rx_kbps, tx_kbps), representing received and transmitted kilobits per second.
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
    with _NET_IO_CACHE_LOCK:
        cache = _NET_IO_CACHE.setdefault(iface, {"counters": cur, "timestamp": now})
        prev = cache.get("counters")
        prev_ts = cache.get("timestamp", now)
        cache["counters"] = cur
        cache["timestamp"] = now
    dt = now - prev_ts if prev_ts else 0.0
    rx_kbps = tx_kbps = 0.0
    if prev is not None and dt > 0:
        rx_kbps = (cur.bytes_recv - prev.bytes_recv) / dt / 1024.0
        tx_kbps = (cur.bytes_sent - prev.bytes_sent) / dt / 1024.0
    return rx_kbps, tx_kbps


def get_smart_status(mount_point: str = '/mnt/ssd') -> str | None:
    """
    Returns the SMART health status of the storage device mounted at the specified path.
    
    Parameters:
        mount_point (str): The mount point of the device to check. Defaults to '/mnt/ssd'.
    
    Returns:
        str | None: A simplified SMART status string ("OK", "FAIL", "WARN"), or None if the device or status cannot be determined.
    """
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
    """
    Converts smartctl command output to a simplified status string ("OK", "FAIL", or "WARN").
    
    Returns:
        str | None: "OK", "FAIL", or "WARN" if recognized keywords are found in the output; otherwise, returns the last line of the output or None if the output is empty.
    """
    for key, val in {"PASSED": "OK", "FAILED": "FAIL", "WARNING": "WARN"}.items():
        if key in output:
            return val
    return output.strip().splitlines()[-1] if output else None


def find_latest_file(directory: str, pattern: str = '*') -> str | None:
    """
    Return the most recently modified file matching a pattern in the specified directory.
    
    Parameters:
    	directory (str): Path to the directory to search.
    	pattern (str): Glob pattern to match files. Defaults to '*' (all files).
    
    Returns:
    	str | None: Path to the newest matching file, or None if no files match.
    """
    dir_path = Path(directory)
    files = list(dir_path.glob(pattern))
    if not files:
        return None
    return str(max(files, key=lambda p: p.stat().st_mtime))


def tail_file(path: str, lines: int = 50) -> list[str]:
    """
    Return the last N lines from a file efficiently using memory mapping.
    
    Parameters:
        path (str): Path to the file to read.
        lines (int): Number of lines to return from the end of the file.
    
    Returns:
        list[str]: The last N lines of the file as a list of strings, or an empty list on error.
    """
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
    """
    Asynchronously retrieves the last specified number of lines from a file.
    
    Parameters:
        path (str): Path to the file to read.
        lines (int): Number of lines to return from the end of the file.
    
    Returns:
        list[str]: The last `lines` lines from the file, or an empty list if the file cannot be read.
    """
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


def _run_systemctl(service: str, action: str) -> tuple[bool, str, str]:
    """
    Run a systemctl command for a given service and action, returning success status and command output.
    
    Parameters:
        service (str): The name of the systemd service (without ".service" suffix).
        action (str): The systemctl action to perform (e.g., "start", "stop", "restart", "is-active").
    
    Returns:
        tuple[bool, str, str]: A tuple containing a boolean indicating success, the command's stdout, and stderr output.
    """

    cmd = ["systemctl", action, f"{service}.service"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, proc.stdout, proc.stderr
    except subprocess.CalledProcessError as exc:  # pragma: no cover - runtime errors
        out = exc.stdout or ""
        err = exc.stderr or str(exc)
        return False, out, err
    except Exception as exc:  # pragma: no cover - unexpected failures
        return False, "", str(exc)


def _run_service_cmd_sync(
    service: str, action: str, attempts: int = 1, delay: float = 0
) -> tuple[bool, str, str]:
    """
    Synchronously execute a systemd service command via DBus, with fallback to systemctl if DBus is unavailable.
    
    Parameters:
        service (str): Name of the systemd service (without '.service' suffix).
        action (str): Action to perform ('start', 'stop', 'restart', or 'is-active').
        attempts (int): Number of retry attempts on failure.
        delay (float): Delay in seconds between retry attempts.
    
    Returns:
        tuple[bool, str, str]: A tuple containing a success flag, output string, and error string.
    """

    try:
        import dbus
    except Exception:  # pragma: no cover - fallback when DBus missing
        return _run_systemctl(service, action)

    from piwardrive.security import validate_service_name

    validate_service_name(service)
    if action not in {"start", "stop", "restart", "is-active"}:
        raise ValueError(f"Invalid action: {action}")

    svc_name = f"{service}.service"

    def _call() -> tuple[bool, str, str]:
        """
        Interact with systemd via DBus to start, stop, restart, or query the status of a service unit.
        
        Returns:
            result (tuple[bool, str, str]): A tuple containing a success flag, the service state or an empty string, and an empty string for error output.
        """
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
    except Exception:
        return _run_systemctl(service, action)


@asynccontextmanager
async def message_bus() -> Any:
    """
    Asynchronous context manager that yields a connected dbus-fast MessageBus instance for system bus communication.
    
    Yields:
        MessageBus: An active dbus-fast MessageBus connected to the system bus.
    """

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
    """
    Asynchronously executes a systemd service command via DBus, with retries and fallback to synchronous execution if DBus is unavailable.
    
    Parameters:
        service (str): The name of the systemd service (without '.service' suffix).
        action (str): The action to perform ('start', 'stop', 'restart', or 'is-active').
        attempts (int): Number of retry attempts on failure.
        delay (float): Delay in seconds between retry attempts.
    
    Returns:
        tuple[bool, str, str]: A tuple containing a success flag, output string (such as service state), and error message (if any).
    """

    from piwardrive.security import validate_service_name

    validate_service_name(service)
    if action not in {"start", "stop", "restart", "is-active"}:
        raise ValueError(f"Invalid action: {action}")

    svc_name = f"{service}.service"

    try:
        import dbus_fast.aio  # type: ignore  # noqa: F401
    except Exception:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, lambda: _run_service_cmd_sync(service, action, attempts, delay)
        )

    async def _call() -> tuple[bool, str, str]:
        """
        Execute a systemd service command asynchronously via DBus and return the result.
        
        Returns:
            A tuple containing a boolean indicating success, the service state or an empty string, and an empty string for error output.
        """
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
        """
        Attempts to execute the asynchronous function `_call` up to `attempts` times, retrying on exception and delaying between attempts if specified.
        
        Returns:
            A tuple containing the result of `_call` if successful.
        
        Raises:
            The last exception encountered if all attempts fail.
        """
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
        return await asyncio.get_running_loop().run_in_executor(
            None, lambda: _run_systemctl(service, action)
        )


def run_service_cmd(
    service: str, action: str, attempts: int = 1, delay: float = 0
) -> tuple[bool, str, str]:
    """
    Synchronously executes a systemd service command and returns the result.
    
    Runs the specified action (e.g., 'start', 'stop', 'restart', 'is-active') on the given service by invoking the asynchronous command runner in a blocking manner. Returns a tuple containing the success status, standard output, and standard error from the command execution.
    
    Returns:
        tuple[bool, str, str]: A tuple of (success, stdout, stderr).
    """

    fut = run_async_task(
        _run_service_cmd_async(service, action, attempts=attempts, delay=delay)
    )
    try:
        ok, out, err = fut.result()
        if not ok:
            if out:
                logging.error("%s %s stdout: %s", service, action, out.strip())
            if err:
                logging.error("%s %s stderr: %s", service, action, err.strip())
        return ok, out, err
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
    """
    Asynchronously checks if a systemd service is active.
    
    Parameters:
        service (str): Name of the systemd service to check.
    
    Returns:
        bool: True if the service is active, False otherwise.
    """
    from piwardrive.security import validate_service_name

    validate_service_name(service)
    try:
        ok, out, _err = await _run_service_cmd_async(
            service, "is-active", attempts=attempts, delay=delay
        )
        return ok and out.strip() == "active"
    except Exception:
        return False


def service_status(service: str, attempts: int = 1, delay: float = 0) -> bool:
    """
    Return True if the specified systemd service is active.
    
    Parameters:
        service (str): The name of the systemd service to check.
    
    Returns:
        bool: True if the service is active, False otherwise.
    """
    fut = run_async_task(
        service_status_async(service, attempts=attempts, delay=delay)
    )
    return fut.result()


def scan_bt_devices() -> list[BluetoothDevice]:
    """
    Scans for nearby Bluetooth devices using DBus and returns a list of discovered devices.
    
    Returns:
        A list of BluetoothDevice objects representing detected Bluetooth devices, including address, name, and optional latitude and longitude if available. Returns an empty list if scanning is disabled or an error occurs.
    """
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
    Return the current local time as a string in 'YYYY-MM-DD HH:MM:SS' format.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def fetch_kismet_devices() -> tuple[list, list]:
    """
    Fetches Kismet device data synchronously by running the asynchronous device fetcher.
    
    Returns:
        A tuple containing two lists: the first with access point data and the second with client device data.
    """

    fut = run_async_task(fetch_kismet_devices_async())
    return fut.result()


async def fetch_kismet_devices_async() -> tuple[list, list]:
    """
    Asynchronously retrieves access point and client device data from the local Kismet API.
    
    Attempts to fetch device information from multiple Kismet API endpoints using HTTP requests. If successful, returns lists of access points and clients, and updates the local AP cache. If the API is unavailable or returns invalid data, falls back to returning cached access points if available; otherwise, returns empty lists.
    
    Returns:
        aps (list): List of access point dictionaries from Kismet.
        clients (list): List of client device dictionaries from Kismet.
    """

    if network_scanning_disabled():
        return [], []

    urls = [
        "http://127.0.0.1:2501/kismet/devices/all.json",
        "http://127.0.0.1:2501/devices/all.json",
    ]
    timeout = aiohttp.ClientTimeout(total=5)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async def _fetch(url: str) -> dict | None:
            """
            Asynchronously fetches JSON data from the specified URL.
            
            Attempts to retrieve and parse JSON from the given URL using an async HTTP session. Returns the parsed dictionary on success, or None if the request fails or the response is not valid JSON. Errors are reported using the application's error reporting mechanism.
            """
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        try:
                            return fastjson.loads(text)
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
    """
    Asynchronously fetches Kismet device data and BetterCAP handshake count in parallel.
    
    Parameters:
        log_folder (str): Path to the directory containing Kismet and BetterCAP logs.
    
    Returns:
        tuple: A tuple containing a list of access points, a list of clients, and the count of BetterCAP handshake files.
    """
    if network_scanning_disabled():
        return [], [], 0
    aps_clients = fetch_kismet_devices_async()
    handshake = asyncio.to_thread(count_bettercap_handshakes, log_folder)
    aps, clients = await aps_clients
    count = await handshake
    return aps, clients, count


def count_bettercap_handshakes(
    log_folder: str = '/mnt/ssd/kismet_logs',
    *,
    cache_seconds: float = HANDSHAKE_CACHE_SECONDS,
) -> int:
    """
    Return the number of BetterCAP handshake `.pcap` files found under the specified log folder, using caching to avoid redundant filesystem scans.
    
    Parameters:
        log_folder (str): Path to the directory containing BetterCAP logs.
        cache_seconds (float): Duration in seconds to cache the handshake count.
    
    Returns:
        int: The number of handshake `.pcap` files found.
    """
    now = time.time()
    cached = _HANDSHAKE_CACHE.get(log_folder)
    if cache_seconds and cached:
        ts, count = cached
        if now - ts <= cache_seconds:
            return count
    try:
        pattern = os.path.join(log_folder, '*_bettercap', '**', '*.pcap')
        files = glob.glob(pattern, recursive=True)
        count = len(files)
    except OSError:
        count = 0
    _HANDSHAKE_CACHE[log_folder] = (now, count)
    return count


def _get_cached_gps_data(force_refresh: bool = False) -> dict[str, Any] | None:
    """
    Returns cached GPSD data containing accuracy and fix quality, refreshing from the GPS client if the cache is stale or forced.
    
    Parameters:
    	force_refresh (bool): If True, forces a refresh from the GPS client even if cached data is still valid.
    
    Returns:
    	dict[str, Any] | None: Dictionary with GPS accuracy, fix quality, and timestamp, or None if no valid data is available.
    """
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
    """
    Returns the current GPS accuracy value from cached GPSD data.
    
    Parameters:
        force_refresh (bool): If True, refreshes the GPSD data cache before retrieving accuracy.
    
    Returns:
        float | None: The GPS accuracy in meters, or None if unavailable.
    """
    data = _get_cached_gps_data(force_refresh)
    if not data:
        return None
    return data.get("accuracy")


def get_gps_fix_quality(force_refresh: bool = False) -> str:
    """
    Returns a human-readable description of the current GPS fix quality from cached GPSD data.
    
    Parameters:
        force_refresh (bool): If True, refreshes the cached GPS data before retrieving the fix quality.
    
    Returns:
        str: The GPS fix quality as a string, or "Unknown" if unavailable.
    """
    data = _get_cached_gps_data(force_refresh)
    if not data:
        return "Unknown"
    return str(data.get("fix", "Unknown"))


def get_avg_rssi(aps: Iterable[dict[str, Any]]) -> float | None:
    """
    Calculates the average RSSI (signal strength in dBm) from a collection of access point dictionaries.
    
    Parameters:
        aps (Iterable[dict[str, Any]]): Iterable of access point dictionaries, each potentially containing a 'signal_dbm' key.
    
    Returns:
        float | None: The average RSSI value if available, otherwise None if no valid data is found.
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
    """
    Return the most recent GPS accuracy value, optionally forcing a refresh.
    
    Parameters:
        force_refresh (bool): If True, bypasses the cache and retrieves fresh GPS data.
    
    Returns:
        float | None: The current GPS accuracy in meters, or None if unavailable.
    """
    return get_gps_accuracy(force_refresh=force_refresh)


def tail_log_file(path: str, lines: int = 50) -> list[str]:
    """
    Return the last N lines from a log file.
    
    This function is an alias for `tail_file` and retrieves the specified number of lines from the end of the given file.
    
    Parameters:
        path (str): Path to the log file.
        lines (int): Number of lines to return from the end of the file.
    
    Returns:
        list[str]: List of lines from the end of the file.
    """
    return tail_file(path, lines)


def get_recent_bssids(limit: int = 5) -> list[str]:
    """
    Retrieve the most recently observed BSSIDs from Kismet device data.
    
    Parameters:
    	limit (int): Maximum number of BSSIDs to return.
    
    Returns:
    	list[str]: List of BSSIDs sorted by most recent observation, or an empty list on error.
    """
    try:
        aps, _ = fetch_kismet_devices()
        # sort by last_time (epoch) descending
        sorted_aps = sorted(aps, key=lambda ap: ap.get('last_time', 0), reverse=True)
        # extract up to `limit` BSSIDs
        return [ap.get('bssid', 'N/A') for ap in sorted_aps[:limit]]
    except Exception:
        return []


def _haversine_distance_py(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """
    Calculate the great-circle distance in meters between two latitude/longitude points using the haversine formula.
    
    Parameters:
        p1 (tuple[float, float]): The first point as (latitude, longitude).
        p2 (tuple[float, float]): The second point as (latitude, longitude).
    
    Returns:
        float: The distance between the two points in meters.
    """
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
    """
    Calculate the approximate planar area of a polygon defined by latitude and longitude points.
    
    Parameters:
        points (Sequence[tuple[float, float]]): Sequence of (latitude, longitude) tuples representing the polygon vertices.
    
    Returns:
        float: Area of the polygon in square meters. Returns 0.0 if fewer than three points are provided.
    """
    if len(points) < 3:
        return 0.0

    import math

    n = len(points)
    lat0 = sum(p[0] for p in points) / n
    lon0 = sum(p[1] for p in points) / n
    cos_lat0 = math.cos(math.radians(lat0))

    def project(p: tuple[float, float]) -> tuple[float, float]:
        """
        Projects a geographic coordinate (latitude, longitude) to a planar (x, y) coordinate using a simple equirectangular projection centered at (lat0, lon0).
        
        Parameters:
            p (tuple[float, float]): The (latitude, longitude) coordinate to project.
        
        Returns:
            tuple[float, float]: The projected (x, y) coordinate relative to the projection center.
        """
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
    """
    Determine whether a geographic point is inside a polygon using the ray casting algorithm.
    
    Parameters:
        point (tuple[float, float]): The (latitude, longitude) coordinates of the point to test.
        polygon (Sequence[tuple[float, float]]): A sequence of (latitude, longitude) tuples defining the polygon vertices.
    
    Returns:
        bool: True if the point is inside the polygon, False otherwise.
    """
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
    """
    Parses a KML coordinates string into a list of (latitude, longitude) tuples.
    
    Parameters:
        text (str): A string containing KML coordinates, where each coordinate is a comma-separated longitude and latitude pair.
    
    Returns:
        list[tuple[float, float]]: A list of (latitude, longitude) tuples extracted from the input string.
    """
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
    """
    Parses a `.kml` or `.kmz` file and returns a list of geographic features.
    
    Each feature is represented as a dictionary containing its name, type (`Point`, `LineString`, or `Polygon`), and coordinates extracted from the file. For `.kmz` files, the first `.kml` file found within the archive is parsed.
    
    Parameters:
        path (str): Path to the `.kml` or `.kmz` file.
    
    Returns:
        list[dict[str, Any]]: List of features with their names, types, and coordinates.
    """
    import zipfile
    import xml.etree.ElementTree as ET

    def _parse(root: ET.Element) -> list[dict[str, Any]]:
        """
        Parses a KML XML root element and extracts geographic features as a list of dictionaries.
        
        Each feature includes its name, type ("Point", "LineString", or "Polygon"), and coordinates parsed from the KML structure.
        """
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


__all__ = [
    "ErrorCode",
    "network_scanning_disabled",
    "shutdown_async_loop",
    "format_error",
    "report_error",
    "require_id",
    "run_async_task",
    "retry_call",
    "safe_request",
    "ensure_service_running",
    "get_cpu_temp",
    "get_mem_usage",
    "get_disk_usage",
    "get_network_throughput",
    "get_smart_status",
    "find_latest_file",
    "tail_file",
    "async_tail_file",
    "message_bus",
    "run_service_cmd",
    "service_status_async",
    "service_status",
    "scan_bt_devices",
    "now_timestamp",
    "fetch_kismet_devices",
    "fetch_kismet_devices_async",
    "fetch_metrics_async",
    "count_bettercap_handshakes",
    "get_gps_accuracy",
    "get_gps_fix_quality",
    "get_avg_rssi",
    "parse_latest_gps_accuracy",
    "tail_log_file",
    "get_recent_bssids",
    "haversine_distance",
    "polygon_area",
    "point_in_polygon",
    "load_kml",
]
