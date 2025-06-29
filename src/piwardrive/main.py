"""Application entry point providing helpers used by scripts and tests."""

from __future__ import annotations

import asyncio
import logging
import os
import time
from dataclasses import asdict, fields
from typing import Any, Callable

from piwardrive import diagnostics, exception_handler, remote_sync, utils
from piwardrive.config import (CONFIG_PATH, Config, config_mtime, load_config,
                               save_config)
from piwardrive.config_watcher import watch_config
from piwardrive.di import Container
from piwardrive.logconfig import setup_logging
from piwardrive.persistence import (AppState, _db_path, load_app_state,
                                    save_app_state)
from piwardrive.scheduler import PollScheduler
from piwardrive.security import hash_password

logging.getLogger("urllib3").setLevel(logging.WARNING)


class PiWardriveApp:
    """Lightweight application container without GUI dependencies."""

    def __init__(
        self,
        container: Container | None = None,
        service_cmd_runner: Callable[..., tuple[bool, str, str]] | None = None,
    ) -> None:
        self.container = container or Container()
        self._run_service_cmd = service_cmd_runner or utils.run_service_cmd
        self.config_data: Config = load_config()
        self.app_state: AppState = asyncio.run(load_app_state())
        self.last_screen = self.app_state.last_screen
        pw = os.getenv("PW_ADMIN_PASSWORD")
        if pw and not self.config_data.admin_password_hash:
            self.config_data.admin_password_hash = hash_password(pw)
        setup_logging(level=logging.INFO)
        exception_handler.install()
        if not self.container.has("scheduler"):
            self.container.register_instance("scheduler", PollScheduler())
        self.scheduler: PollScheduler = self.container.resolve("scheduler")
        if not self.container.has("health_monitor"):
            self.container.register_instance(
                "health_monitor",
                diagnostics.HealthMonitor(self.scheduler, 10),
            )
        self.health_monitor = self.container.resolve("health_monitor")
        import tile_maintenance

        self.tile_maintainer = tile_maintenance.TileMaintainer(
            self.scheduler,
            folder=os.path.dirname(self.config_data.offline_tile_path)
            or "/mnt/ssd/tiles",
            offline_path=self.config_data.offline_tile_path,
            interval=604800,
            max_age_days=30,
            limit_mb=512,
            vacuum=True,
        )
        if (
            self.config_data.remote_sync_url
            and self.config_data.remote_sync_interval > 0
        ):
            self.scheduler.schedule(
                "remote_sync",
                lambda _dt: utils.run_async_task(
                    remote_sync.sync_database_to_server(
                        _db_path(),
                        self.config_data.remote_sync_url,
                        timeout=self.config_data.remote_sync_timeout,
                        retries=self.config_data.remote_sync_retries,
                    )
                ),
                self.config_data.remote_sync_interval * 60,
            )
        if os.getenv("PW_PROFILE"):
            diagnostics.start_profiling()
        self._config_stamp = config_mtime()
        self._updating_config = False
        self._config_observer: Any = watch_config(
            CONFIG_PATH, lambda: self._reload_config_event(0)
        )

    # ------------------------------------------------------------------
    # Service control with feedback
    def control_service(self, svc: str, action: str) -> None:
        """Run a systemctl command for a given service with retries."""
        import getpass as _getpass

        from piwardrive.security import validate_service_name as _validate
        from piwardrive.security import verify_password as _verify

        cfg_hash = getattr(self.config_data, "admin_password_hash", "")
        pw = os.getenv("PW_ADMIN_PASSWORD")
        if not pw:
            try:
                pw = _getpass.getpass("Password: ")
            except Exception:
                pw = ""
        if cfg_hash and not _verify(pw or "", cfg_hash):
            utils.report_error("Unauthorized")
            return
        try:
            _validate(svc)
        except ValueError as exc:
            utils.report_error(str(exc))
            return
        try:
            success, _out, err = self._run_service_cmd(svc, action, attempts=3, delay=1)
        except Exception as exc:  # pragma: no cover - subprocess failures
            utils.report_error(f"Failed to {action} {svc}: {exc}")
            return
        if not success:
            msg = err.strip() if isinstance(err, str) else err
            utils.report_error(f"Failed to {action} {svc}: {msg or 'Unknown error'}")
            return
        if action in {"start", "restart"} and not utils.ensure_service_running(svc):
            utils.report_error(f"{svc} failed to stay running after {action}")

    async def export_logs(self, path: str | None = None, lines: int = 200) -> str:
        """Write the last ``lines`` from ``app.log`` to ``path`` and return it."""
        from logconfig import DEFAULT_LOG_PATH

        if path is None:
            ts = int(time.time())
            path = os.path.join(os.path.expanduser("~"), f"piwardrive-logs-{ts}.txt")
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            data = "\n".join(utils.tail_file(DEFAULT_LOG_PATH, lines))

            def _write(p: str, content: str) -> None:
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(content)

            await asyncio.to_thread(_write, path, data)
            logging.info("Exported logs to %s", path)
            return path
        except Exception as exc:  # pragma: no cover - file errors
            logging.exception("Failed to export logs: %s", exc)
            utils.report_error(f"Failed to export logs: {exc}")
            return ""

    async def export_log_bundle(self, path: str | None = None, lines: int = 200) -> str:
        """Write the last ``lines`` from each configured log to ``path``."""
        import zipfile

        from logconfig import DEFAULT_LOG_PATH

        from piwardrive.security import sanitize_path

        if path is None:
            ts = int(time.time())
            path = os.path.join(
                os.path.expanduser("~"), f"piwardrive-log-bundle-{ts}.zip"
            )

        log_paths = [DEFAULT_LOG_PATH] + list(self.config_data.log_paths)

        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                for p in log_paths:
                    safe = sanitize_path(p)
                    lines_text = "\n".join(utils.tail_file(safe, lines))
                    zf.writestr(os.path.basename(safe), lines_text)
            logging.info("Exported log bundle to %s", path)
            return path
        except Exception as exc:  # pragma: no cover - file errors
            logging.exception("Failed to export log bundle: %s", exc)
            utils.report_error(f"Failed to export log bundle: {exc}")
            return ""

    def _reload_config_event(self, _dt: float) -> None:
        """Reload settings if ``config.json`` changed."""
        stamp = config_mtime()
        if stamp is None or stamp == self._config_stamp:
            return
        self._config_stamp = stamp
        data = load_config()
        self._updating_config = True
        self.config_data = data
        for key, val in asdict(data).items():
            if hasattr(self, key):
                setattr(self, key, val)
        self._updating_config = False

    def on_stop(self) -> None:
        """Persist configuration values on application exit."""
        if hasattr(self, "_config_observer"):
            self._config_observer.stop()
            self._config_observer.join()
        prof = diagnostics.stop_profiling()
        if prof:
            logging.info("Profiling summary:\n%s", prof)
        for f in fields(Config):
            key = f.name
            if hasattr(self, key):
                setattr(self.config_data, key, getattr(self, key))
        try:
            save_config(self.config_data)
        except OSError as exc:  # pragma: no cover - save failure is non-critical
            logging.exception("Failed to save config: %s", exc)
        try:
            asyncio.run(save_app_state(self.app_state))
        except OSError as exc:  # pragma: no cover - save failure
            logging.exception("Failed to save app state: %s", exc)
        utils.shutdown_async_loop()


def main() -> None:
    """Entry point for backwards compatibility."""
    try:
        PiWardriveApp()
    finally:
        utils.shutdown_async_loop()


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
