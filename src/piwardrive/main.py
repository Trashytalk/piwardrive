"""Main application entry point for the PiWardrive GUI."""

import logging
import os
import time
import asyncio
from dataclasses import asdict, fields

from typing import Any, Callable


from piwardrive.scheduler import PollScheduler
from piwardrive.config import (
    load_config,
    save_config,
    Config,
    config_mtime,
    CONFIG_PATH,
)
from piwardrive.config_watcher import watch_config

from piwardrive.security import hash_password
from piwardrive.persistence import (
    save_app_state,
    load_app_state,
    AppState,
    _db_path,
)
from piwardrive import remote_sync

from piwardrive import diagnostics
from piwardrive import utils
from piwardrive.di import Container
from piwardrive.logconfig import setup_logging
from piwardrive import exception_handler

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import (  # pylint: disable=no-name-in-module
    BooleanProperty,
    NumericProperty,
    StringProperty,
    ListProperty,
)
from kivymd.app import MDApp

# Trim down HTTP debug logging

from piwardrive.screens.console_screen import ConsoleScreen  # type: ignore[import]
from piwardrive.screens.dashboard_screen import (
    DashboardScreen,  # type: ignore[import]
)
from piwardrive.screens.map_screen import MapScreen  # type: ignore[import]
from piwardrive.screens.settings_screen import (
    SettingsScreen,  # type: ignore[import]
)
from piwardrive.screens.split_screen import SplitScreen  # type: ignore[import]
from piwardrive.screens.stats_screen import StatsScreen  # type: ignore[import]

logging.getLogger("urllib3").setLevel(logging.WARNING)


class PiWardriveApp(MDApp):
    """Main application class handling screen setup and helpers."""

    map_poll_gps = NumericProperty(10)
    map_poll_gps_max = NumericProperty(30)
    map_poll_aps = NumericProperty(60)
    map_poll_bt = NumericProperty(60)
    map_poll_wigle = NumericProperty(0)
    map_show_gps = BooleanProperty(True)
    map_follow_gps = BooleanProperty(True)
    map_show_aps = BooleanProperty(True)
    map_show_bt = BooleanProperty(False)
    map_show_wigle = BooleanProperty(False)
    map_cluster_aps = BooleanProperty(False)
    map_cluster_capacity = NumericProperty(8)
    map_fullscreen = BooleanProperty(False)
    map_use_offline = BooleanProperty(False)
    map_auto_prefetch = BooleanProperty(False)
    disable_scanning = BooleanProperty(False)
    theme = StringProperty("Dark")
    kismet_logdir = StringProperty("/mnt/ssd/kismet_logs")
    bettercap_caplet = StringProperty("/usr/local/etc/bettercap/alfa.cap")
    wigle_api_name = StringProperty("")
    wigle_api_key = StringProperty("")
    dashboard_layout = ListProperty([])
    debug_mode = BooleanProperty(False)
    widget_disk_trend = BooleanProperty(True)
    widget_cpu_temp = BooleanProperty(True)
    widget_net_throughput = BooleanProperty(True)
    widget_battery_status = BooleanProperty(False)
    widget_health_analysis = BooleanProperty(True)
    ui_font_size = NumericProperty(16)
    log_paths = ListProperty(
        [
            "/var/log/syslog",
            "/var/log/kismet.log",
            "/var/log/bettercap.log",
        ]
    )
    health_poll_interval = NumericProperty(10)
    log_rotate_interval = NumericProperty(3600)
    log_rotate_archives = NumericProperty(3)
    cleanup_rotated_logs = BooleanProperty(True)
    tile_maintenance_interval = NumericProperty(604800)
    tile_max_age_days = NumericProperty(30)
    tile_cache_limit_mb = NumericProperty(512)
    compress_offline_tiles = BooleanProperty(True)
    route_prefetch_interval = NumericProperty(3600)
    route_prefetch_lookahead = NumericProperty(5)
    last_screen = StringProperty("Map")

    def __init__(
        self,
        container: Container | None = None,
        service_cmd_runner: Callable[..., tuple[bool, str, str]] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.container = container or Container()
        self._run_service_cmd = service_cmd_runner or utils.run_service_cmd

        # load persisted configuration
        self.config_data: Config = load_config()
        self.app_state: AppState = asyncio.run(load_app_state())
        self.last_screen = self.app_state.last_screen
        for key, val in asdict(self.config_data).items():
            if hasattr(self, key):
                setattr(self, key, val)

        pw = os.getenv("PW_ADMIN_PASSWORD")
        if pw and not self.config_data.admin_password_hash:
            self.config_data.admin_password_hash = hash_password(pw)

        setup_logging(level=logging.DEBUG if self.debug_mode else logging.INFO)
        exception_handler.install()

        if not self.container.has("scheduler"):
            self.container.register_instance("scheduler", PollScheduler())
        self.scheduler = self.container.resolve("scheduler")

        if not self.container.has("health_monitor"):
            self.container.register_instance(
                "health_monitor",
                diagnostics.HealthMonitor(self.scheduler, self.health_poll_interval),
            )
        self.health_monitor = self.container.resolve("health_monitor")
        import tile_maintenance
        self.tile_maintainer = tile_maintenance.TileMaintainer(
            self.scheduler,
            folder=os.path.dirname(self.offline_tile_path) or "/mnt/ssd/tiles",
            offline_path=self.offline_tile_path,
            interval=self.tile_maintenance_interval,
            max_age_days=self.tile_max_age_days,
            limit_mb=self.tile_cache_limit_mb,
            vacuum=self.compress_offline_tiles,
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
        self.theme_cls.theme_style = self.theme
        self._config_stamp = config_mtime()
        self._updating_config = False
        self._config_observer = watch_config(
            CONFIG_PATH, lambda: self._reload_config_event(0)
        )
        for f in fields(Config):
            if hasattr(self.__class__, f.name):
                self.bind(**{f.name: lambda _i, v, k=f.name: self._auto_save(k, v)})

    def build(self) -> Any:
        """Load and return the root widget tree from KV."""
        root = Builder.load_file("kv/main.kv")
        self.root = root
        return root

    def on_start(self) -> None:
        """Initialize screens and navigation on start."""
        # DEBUG: show which IDs were parsed from KV if debug mode is enabled
        if self.debug_mode:
            print("Root IDs:", self.root.ids.keys())
        sm = utils.require_id(self.root, "sm")
        nav_bar = utils.require_id(self.root, "nav_bar")

        # 1) Add all six screens first
        sm.add_widget(MapScreen(name="Map"))  # type: ignore[call-arg]
        sm.add_widget(StatsScreen(name="Stats"))  # type: ignore[call-arg]
        sm.add_widget(SplitScreen(name="Split"))  # type: ignore[call-arg]
        sm.add_widget(ConsoleScreen(name="Console"))  # type: ignore[call-arg]
        sm.add_widget(SettingsScreen(name="Settings"))  # type: ignore[call-arg]
        sm.add_widget(DashboardScreen(name="Dashboard"))  # type: ignore[call-arg]

        # 2) Now set the initial screen explicitly from persisted state
        sm.current = self.last_screen

        # 3) Build your responsive nav buttons
        for name in ["Map", "Stats", "Split", "Console", "Settings", "Dashboard"]:
            btn = Factory.NavigationButton(
                text=name, on_release=lambda btn, s=name: self.switch_screen(s)
            )
            nav_bar.add_widget(btn)
        map_screen = sm.get_screen("Map")
        import route_prefetch
        self.route_prefetcher = route_prefetch.RoutePrefetcher(
            self.scheduler,
            map_screen,
            interval=self.route_prefetch_interval,
            lookahead=self.route_prefetch_lookahead,
        )
        if self.cleanup_rotated_logs:
            for path in self.log_paths:
                ev = f"rotate_{os.path.basename(path)}"
                self.scheduler.schedule(
                    ev,
                    lambda _dt, p=path: diagnostics.rotate_log_async(
                        p, self.log_rotate_archives
                    ),
                    self.log_rotate_interval,
                )

    def switch_screen(self, name: str) -> None:
        """Change the active screen."""
        utils.require_id(self.root, "sm").current = name
        self.last_screen = name
        self.app_state.last_screen = name
        asyncio.run(save_app_state(self.app_state))

    # 1) Service control with feedback
    def control_service(self, svc: str, action: str) -> None:
        """Run a systemctl command for a given service with retries."""
        import os as _os
        import getpass as _getpass
        from piwardrive.security import (
            verify_password as _verify,
            validate_service_name as _validate,
        )

        cfg_hash = getattr(
            getattr(self, "config_data", None),
            "admin_password_hash",
            "",
        )
        pw = _os.getenv("PW_ADMIN_PASSWORD")
        if not pw:
            try:
                pw = _getpass.getpass("Password: ")
            except Exception:  # pragma: no cover - prompt failures
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

    def show_alert(self, title: str, text: str) -> None:
        """Display a simple alert dialog with the given title and text."""
        from kivymd.uix.dialog import MDDialog

        dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.8, None),
            buttons=[],
        )
        dialog.open()

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

    def _auto_save(self, key: str, value: Any) -> None:
        """Update ``config_data`` and persist to disk."""
        if self._updating_config:
            return
        if hasattr(self.config_data, key):
            setattr(self.config_data, key, value)
            try:
                save_config(self.config_data)
            except OSError as exc:  # pragma: no cover - write errors
                logging.exception("Failed to auto-save config: %s", exc)

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
    """Launch :class:`PiWardriveApp`."""
    try:
        PiWardriveApp().run()
    finally:
        utils.shutdown_async_loop()


if __name__ == "__main__":
    main()
