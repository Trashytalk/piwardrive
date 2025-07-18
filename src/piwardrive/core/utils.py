"""Utility functions for the PiWardrive GUI application."""

# pylint: disable=broad-exception-caught,unspecified-encoding,subprocess-run-check

import asyncio
import functools
import glob
import logging
import mmap
import os
import pickle
import subprocess
import threading
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Iterable,
    Sequence,
    TypedDict,
    TypeVar,
)

from piwardrive import config as pw_config
from piwardrive.gpsd_client import client as gps_client

from . import fastjson

try:  # pragma: no cover - optional dependency
    from piwardrive.sigint_suite.models import BluetoothDevice
except ImportError:  # pragma: no cover - fallback when sigint_suite is missing
    BluetoothDevice = dict[str, Any]
from concurrent.futures import Future
from enum import IntEnum

import psutil
import requests
from cachetools import TTLCache

try:  # pragma: no cover - optional dependency
    import redis.asyncio as aioredis
except Exception:  # pragma: no cover - redis not installed
    aioredis = None

try:
    import requests_cache
except ImportError:  # pragma: no cover - optional dependency
    requests_cache = None
import aiohttp

from piwardrive import persistence
from piwardrive.cache_config import load_cache_config


class App:
    """Placeholder application interface."""

    @staticmethod
    def get_running_app() -> None:
        """Return ``None`` when no GUI is active."""
        return None


GPSD_CACHE_SECONDS = 2.0  # cache ttl in seconds


class _GPSDEntry(TypedDict):
    timestamp: float
    accuracy: float | None
    fix: str


_GPSD_CACHE: _GPSDEntry = {
    "timestamp": 0.0,
    "accuracy": None,
    "fix": "Unknown",
}

# Track previous network counters for throughput calculations
# psutil may be replaced with a mock in tests. Avoid touching internals at
# runtime to prevent import errors when ``psutil._common`` is missing.
if TYPE_CHECKING:  # pragma: no cover - typing only
    from psutil._common import snetio as _SnetIO
else:  # pragma: no cover - runtime fallback
    _SnetIO = object


class _NetIOEntry(TypedDict):
    timestamp: float
    counters: _SnetIO


_NET_IO_CACHE: dict[str | None, _NetIOEntry] = {
    None: {
        "timestamp": time.time(),
        "counters": psutil.net_io_counters(),
    }
}

_NET_IO_CACHE_LOCK = threading.Lock()
# Cache for frequently polled system metrics
MEM_USAGE_CACHE_SECONDS = 2.0


class _MemUsageEntry(TypedDict):
    timestamp: float
    percent: float | None


_MEM_USAGE_CACHE: _MemUsageEntry = {"timestamp": 0.0, "percent": None}

DISK_USAGE_CACHE_SECONDS = 2.0


class _DiskUsageEntry(TypedDict):
    timestamp: float
    percent: float | None


_DISK_USAGE_CACHE: dict[str, _DiskUsageEntry] = {}

# Cache for HTTP requests issued via :func:`safe_request`
# Default TTL in seconds and maximum cache size. ``cachetools.TTLCache``
# handles automatic eviction without blocking individual requests.
SAFE_REQUEST_CACHE_SECONDS = 10.0
SAFE_REQUEST_CACHE_MAX_SIZE = 128
_SAFE_REQUEST_CACHE: TTLCache[str, requests.Response | Any] = TTLCache(
    maxsize=SAFE_REQUEST_CACHE_MAX_SIZE, ttl=SAFE_REQUEST_CACHE_SECONDS
)

_SAFE_REQUEST_CACHE_LOCK = threading.Lock()

# Optional Redis client for cross-process caching
_REDIS_CLIENT: "aioredis.Redis | None" = None


def _get_redis_client() -> "aioredis.Redis | None":
    """Return Redis client using env or ``cache_config.json`` settings."""
    global _REDIS_CLIENT
    if _REDIS_CLIENT is not None:
        return _REDIS_CLIENT
    url = os.getenv("PIWARDRIVE_REDIS_URL")
    if not url:
        cfg = load_cache_config().get("redis", {})
        url = cfg.get("url")
    if not url or aioredis is None:
        return None
    try:
        cfg = load_cache_config().get("redis", {})
        max_conn = cfg.get("max_connections")
        kwargs = {"max_connections": int(max_conn)} if max_conn else {}
        _REDIS_CLIENT = aioredis.from_url(url, **kwargs)
    except Exception:  # pragma: no cover - Redis misconfiguration
        logging.exception("Failed to initialize Redis client")
        _REDIS_CLIENT = None
    return _REDIS_CLIENT


def _safe_request_cache_pruner() -> None:
    """Background task expiring old safe request cache entries."""
    while True:
        time.sleep(SAFE_REQUEST_CACHE_SECONDS)
        _expire_safe_request_cache()


_safe_request_cache_pruner_thread = threading.Thread(
    target=_safe_request_cache_pruner,
    daemon=True,
    name="safe_request_cache_pruner",
)
_safe_request_cache_pruner_thread.start()

# Cache for BetterCAP handshake counts
HANDSHAKE_CACHE_SECONDS = pw_config.DEFAULT_CONFIG.handshake_cache_seconds
_HANDSHAKE_CACHE: dict[str, tuple[float, float, int]] = {}
_HANDSHAKE_CACHE_LOCK = threading.Lock()

# Cache for tail_file results
TAIL_FILE_CACHE_SECONDS = pw_config.DEFAULT_CONFIG.log_tail_cache_seconds
_TAIL_FILE_CACHE: dict[str, tuple[float, float, list[str]]] = {}
_TAIL_FILE_CACHE_LOCK = threading.Lock()

# Cache for service endpoint data
KISMET_CACHE_SECONDS = 2.0
WIGLE_CACHE_SECONDS = 30.0

if requests_cache is not None:
    HTTP_SESSION = requests_cache.CachedSession(expire_after=SAFE_REQUEST_CACHE_SECONDS)
else:  # pragma: no cover - fallback without requests_cache

    class _DummySession:
        def get(self, *args: Any, **kwargs: Any) -> Any:
            """Fallback ``requests.get`` with a default timeout."""
            timeout = kwargs.pop("timeout", 5)
            return requests.get(*args, timeout=timeout, **kwargs)

    HTTP_SESSION = _DummySession()

T = TypeVar("T")


def _expire_safe_request_cache() -> None:
    """Clean up expired cache entries without blocking requests."""
    with _SAFE_REQUEST_CACHE_LOCK:
        _SAFE_REQUEST_CACHE.expire()


def async_ttl_cache(
    ttl_getter: float | Callable[[], float],
) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]:
    """Return decorator caching async function results for ``ttl`` seconds."""

    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        cache: dict[tuple[Any, ...], tuple[float, T]] = {}
        lock = asyncio.Lock()

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            ttl = ttl_getter() if callable(ttl_getter) else ttl_getter
            key = (args, tuple(sorted(kwargs.items())))
            try:
                now = time.time()
            except Exception:
                # In tests ``time.time`` may be replaced by a side effect that
                # runs out of values. Skip caching in that case.
                now = None
            async with lock:
                entry = cache.get(key)
                if entry and now is not None and now - entry[0] <= ttl:
                    return entry[1]
            redis_cli = _get_redis_client()
            redis_key = None
            if redis_cli is not None:
                redis_key = f"async_cache:{func.__module__}:{func.__name__}:{hash(key)}"
                try:
                    data = await redis_cli.get(redis_key)
                    if data:
                        ts, res = pickle.loads(data)
                        if now is not None and now - ts <= ttl:
                            return res
                except Exception:
                    logging.debug("Redis get failed", exc_info=True)
            result = await func(*args, **kwargs)
            async with lock:
                cache[key] = ((0.0 if now is None else now), result)
            if redis_cli is not None and redis_key is not None:
                try:
                    await redis_cli.set(
                        redis_key,
                        pickle.dumps((0.0 if now is None else now, result)),
                        ex=int(ttl),
                    )
                except Exception:
                    logging.debug("Redis set failed", exc_info=True)
            return result

        return wrapper

    return decorator


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

    ``requests_cache`` handles caching using :data:`HTTP_SESSION`.
    The ``cache_seconds`` argument controls the per-request expiration.
    Passing ``cache_seconds`` as ``0`` disables caching.
    """
    if cache_seconds:
        with _SAFE_REQUEST_CACHE_LOCK:
            cached = _SAFE_REQUEST_CACHE.get(url)
        if cached is not None:
            return cached

    def _get() -> Any:
        return HTTP_SESSION.get(
            url,
            timeout=timeout,
            expire_after=cache_seconds or None,
            **kwargs,
        )

    try:
        resp = retry_call(_get, attempts=attempts, delay=1)
        resp.raise_for_status()
        if cache_seconds:
            with _SAFE_REQUEST_CACHE_LOCK:
                _SAFE_REQUEST_CACHE[url] = resp
        return resp
    except requests.Timeout as exc:
        report_error(f"Request timeout for {url}: {exc}")
    except requests.HTTPError as exc:
        status = (
            exc.response.status_code if getattr(exc, "response", None) else "Unknown"
        )
        report_error(f"HTTP {status} error for {url}: {exc}")
    except requests.RequestException as exc:
        report_error(f"Request exception for {url}: {exc}")
    except Exception as exc:  # pragma: no cover - unexpected errors
        report_error(f"Unexpected error for {url}: {exc}")
    if fallback is not None:
        try:
            result = fallback()
            if cache_seconds:
                with _SAFE_REQUEST_CACHE_LOCK:
                    _SAFE_REQUEST_CACHE[url] = result
            return result
        except Exception as exc2:  # pragma: no cover - fallback failed
            report_error(f"Fallback for {url} failed: {exc2}")
    return None


def ensure_service_running(
    service: str, *, attempts: int = 3, delay: float = 1.0
) -> bool:
    """Ensure ``service`` is active, attempting a restart if not."""
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
    """Read the Raspberry Pi CPU temperature from sysfs.

    Returns temperature in °C as a float, or None on failure.
    """
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_str = f.read().strip()
        return float(temp_str) / 1000.0
    except (OSError, ValueError):
        return None


def get_mem_usage() -> float | None:
    """Return system memory usage percentage."""
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


def get_disk_usage(path: str = "/mnt/ssd") -> float | None:
    """Return disk usage percentage for given path."""
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


def get_smart_status(mount_point: str = "/mnt/ssd") -> str | None:
    """Return SMART health status for the device mounted at ``mount_point``."""
    try:
        dev = next(
            (
                p.device
                for p in psutil.disk_partitions(all=False)
                if p.mountpoint == mount_point
            ),
            None,
        )
        if not dev:
            return None
        try:
            proc = subprocess.run(
                ["smartctl", "-H", dev],
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


def find_latest_file(directory: str, pattern: str = "*") -> str | None:
    """Return the newest file matching ``pattern`` under ``directory``."""
    dir_path = Path(directory)
    files = list(dir_path.glob(pattern))
    if not files:
        return None
    return str(max(files, key=lambda p: p.stat().st_mtime))


def tail_file(path: str, lines: int = 50) -> list[str]:
    """Return the last ``lines`` from ``path`` efficiently using ``mmap``."""
    if lines <= 0:
        return []
    now = time.time()
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        mtime = 0.0
    with _TAIL_FILE_CACHE_LOCK:
        cached = _TAIL_FILE_CACHE.get(path)
        if cached:
            ts, cached_mtime, data = cached
            if now - ts <= TAIL_FILE_CACHE_SECONDS and cached_mtime == mtime:
                return data[-lines:]
    try:
        with (
            open(path, "rb") as f,
            mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm,
        ):
            pos = mm.size()
            for _ in range(lines + 1):
                new_pos = mm.rfind(b"\n", 0, pos)
                if new_pos == -1:
                    pos = -1
                    break
                pos = new_pos
            start = 0 if pos < 0 else pos + 1
            text = mm[start:]
            _result = text.decode("utf-8", errors="ignore").splitlines()
    except (OSError, ValueError):
        pass
    with _TAIL_FILE_CACHE_LOCK:
        _TAIL_FILE_CACHE[path] = (now, mtime, _result)
    return _result[-lines:]


async def async_tail_file(path: str, lines: int = 50) -> list[str]:
    """Asynchronously return the last ``lines`` from ``path``."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: tail_file(path, lines))


def _run_systemctl(service: str, action: str) -> tuple[bool, str, str]:
    """Fallback ``systemctl`` invocation capturing output."""
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
    """Execute DBus service commands synchronously as a fallback."""
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
    """Yield a connected ``dbus-fast`` ``MessageBus`` instance."""
    from dbus_fast import BusType
    from dbus_fast.aio import MessageBus

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
    from piwardrive.security import validate_service_name

    validate_service_name(service)
    if attempts <= 0:
        raise ValueError("attempts must be >= 1")
    if action not in {"start", "stop", "restart", "is-active"}:
        raise ValueError(f"Invalid action: {action}")

    svc_name = f"{service}.service"

    try:
        import dbus_fast.aio  # noqa: F401
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
            unit = bus.get_proxy_object("org.freedesktop.systemd1", unit_path, uintro)
            props = unit.get_interface("org.freedesktop.DBus.Properties")
            state = await props.call_get("org.freedesktop.systemd1.Unit", "ActiveState")
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
        logging.exception("Service command '%s %s' failed: %s", service, action, exc)
        return False, "", str(exc)


def run_service_cmd(
    service: str, action: str, attempts: int = 1, delay: float = 0
) -> tuple[bool, str, str]:
    """Run ``_run_service_cmd_async`` in a synchronous context."""
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
    """Return ``True`` if the ``systemd`` service is active."""
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
    """Check a service's status using the asynchronous helper."""
    fut = run_async_task(service_status_async(service, attempts=attempts, delay=delay))
    return fut.result()


def scan_bt_devices() -> list[BluetoothDevice]:
    """Return nearby Bluetooth devices via DBus."""
    if network_scanning_disabled():
        return []
    try:
        import dbus

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
    """Return the current time as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def fetch_kismet_devices() -> tuple[list, list]:
    """Synchronize Kismet device data using the async helper."""
    fut = run_async_task(fetch_kismet_devices_async())
    return fut.result()


@async_ttl_cache(lambda: KISMET_CACHE_SECONDS)
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
                            f"Kismet API request failed: {exc}. ",
                            "Ensure Kismet is running.",
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


@dataclass
class MetricsResult:
    """Results from :func:`fetch_metrics_async`."""

    aps: list[Any]
    clients: list[Any]
    handshake_count: int


async def fetch_metrics_async(
    log_folder: str = "/mnt/ssd/kismet_logs",
) -> MetricsResult:
    """Fetch Kismet devices and BetterCAP handshake count concurrently."""
    if network_scanning_disabled():
        return MetricsResult([], [], 0)
    aps_clients = fetch_kismet_devices_async()
    handshake = asyncio.to_thread(count_bettercap_handshakes, log_folder)
    aps, clients = await aps_clients
    count = await handshake
    return MetricsResult(aps, clients, count)


def count_bettercap_handshakes(
    log_folder: str = "/mnt/ssd/kismet_logs",
    *,
    cache_seconds: float = HANDSHAKE_CACHE_SECONDS,
) -> int:
    """Return handshake count using caching and glob lookup."""
    now = time.time()
    with _HANDSHAKE_CACHE_LOCK:
        cached = _HANDSHAKE_CACHE.get(log_folder)
        if cache_seconds and cached:
            ts, mtime, count = cached
            try:
                cur_mtime = os.path.getmtime(log_folder)
            except OSError:
                cur_mtime = 0.0
            if now - ts <= cache_seconds and mtime >= cur_mtime:
                return count
    try:
        pattern = os.path.join(log_folder, "*_bettercap", "**", "*.pcap")
        files = glob.glob(pattern, recursive=True)
        count = len(files)
    except OSError:
        count = 0
    try:
        folder_mtime = os.path.getmtime(log_folder)
    except OSError:
        folder_mtime = 0.0
    with _HANDSHAKE_CACHE_LOCK:
        _HANDSHAKE_CACHE[log_folder] = (now, folder_mtime, count)
    return count


def _get_cached_gps_data(force_refresh: bool = False) -> _GPSDEntry | None:
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
    """Compute average RSSI (signal_dbm) from a list of access_points.

    Returns float average or None if no data.
    """
    try:
        vals = []
        for ap in aps:
            val = ap.get("signal_dbm")
            if val is not None:
                vals.append(float(val))
        return sum(vals) / len(vals) if vals else None
    except Exception:
        return None


def parse_latest_gps_accuracy(force_refresh: bool = False) -> float | None:
    """Alias for :func:`get_gps_accuracy`."""
    return get_gps_accuracy(force_refresh=force_refresh)


def tail_log_file(path: str, lines: int = 50) -> list[str]:
    """Alias for tail_file."""
    return tail_file(path, lines)


def get_recent_bssids(limit: int = 5) -> list[str]:
    """Return the most recently observed BSSIDs from the Kismet API."""
    try:
        aps, _ = fetch_kismet_devices()
        # sort by last_time (epoch) descending
        sorted_aps = sorted(aps, key=lambda ap: ap.get("last_time", 0), reverse=True)
        # extract up to `limit` BSSIDs
        return [ap.get("bssid", "N/A") for ap in sorted_aps[:limit]]
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
        if (lon1 > lon) != (lon2 > lon):
            intersect = (lat2 - lat1) * (lon - lon1) / (lon2 - lon1 + 1e-12) + lat1
            if lat < intersect:
                inside = not inside
    return inside


try:  # pragma: no cover - optional geometry C extension for speed
    from cgeom import haversine_distance as _haversine_distance_c
    from cgeom import point_in_polygon as _point_in_polygon_c
    from cgeom import polygon_area as _polygon_area_c
except Exception:  # pragma: no cover - extension not built
    _haversine_distance_c = None
    _polygon_area_c = None
    _point_in_polygon_c = None

haversine_distance = _haversine_distance_c or _haversine_distance_py
polygon_area = _polygon_area_c or _polygon_area_py
point_in_polygon = _point_in_polygon_c or _point_in_polygon_py

try:  # pragma: no cover - optional C extension for speed
    from ckml import parse_coords as _parse_coords
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

    from defusedxml import ElementTree as ET

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
                feats.append(
                    {
                        "name": name,
                        "type": "LineString",
                        "coordinates": coords,
                    }
                )
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
    "MetricsResult",
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
    "SAFE_REQUEST_CACHE_MAX_SIZE",
    "HTTP_SESSION",
]
