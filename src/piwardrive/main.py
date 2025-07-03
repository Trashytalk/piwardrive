"""Application entry point providing helpers used by scripts and tests."""

from __future__ import annotations

import asyncio
import logging
import os
import subprocess
import time
from dataclasses import asdict, fields
from pathlib import Path
from typing import Callable

from watchdog.observers import Observer

from piwardrive import diagnostics, exception_handler, notifications, remote_sync, utils
from piwardrive.config import (
    CONFIG_PATH,
    Config,
    config_mtime,
    load_config,
    save_config,
)
from piwardrive.config_watcher import watch_config
from piwardrive.di import Container
from piwardrive.logging import init_logging
from piwardrive.persistence import AppState, _db_path, load_app_state, save_app_state
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
        init_logging()
        exception_handler.install()
        if not self.container.has("scheduler"):
            self.container.register_instance("scheduler", PollScheduler())
        self.scheduler: PollScheduler = self.container.resolve("scheduler")
        mqtt_client = None
        if self.config_data.enable_mqtt:
            from piwardrive.mqtt import MQTTClient

            mqtt_client = MQTTClient()
            mqtt_client.connect()
        self.mqtt_client = mqtt_client
        if not self.container.has("health_monitor"):
            self.container.register_instance(
                "health_monitor",
                diagnostics.HealthMonitor(self.scheduler, 10, mqtt_client=mqtt_client),
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
        try:
            from piwardrive import scan_report

            self.scheduler.schedule(
                "scan_report",
                lambda _dt: utils.run_async_task(scan_report.write_scan_report()),
                86400,
            )
        except Exception:
            logging.exception("Failed to schedule scan report")
        update_hours = int(os.getenv("PW_UPDATE_INTERVAL", "0"))
        if update_hours > 0:
            script = Path(__file__).resolve().parents[2] / "scripts" / "update.sh"

            async def _run_update() -> None:
                try:
                    proc = await asyncio.create_subprocess_exec(str(script))
                    await proc.wait()
                    if proc.returncode != 0:
                        logging.error("Updater exited with %s", proc.returncode)
                except Exception as exc:
                    logging.exception("Failed to run updater: %s", exc)

            self.scheduler.schedule(
                "auto_update",
                lambda _dt: utils.run_async_task(_run_update()),
                update_hours * 3600,
            )

        self.notifications = notifications.NotificationManager(
            self.scheduler,
            webhooks=self.config_data.notification_webhooks,
            cpu_temp_threshold=self.config_data.notify_cpu_temp,
            disk_percent_threshold=self.config_data.notify_disk_percent,
        )
        if os.getenv("PW_PROFILE"):
            diagnostics.start_profiling()
        self._config_stamp = config_mtime()
        self._updating_config = False
        self._config_observer: Observer = watch_config(
            CONFIG_PATH, lambda: self._reload_config_event(0)
        )

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
