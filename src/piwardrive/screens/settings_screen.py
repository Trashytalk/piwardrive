"""Simplified settings screen used in tests."""

from __future__ import annotations

import os
from types import SimpleNamespace
from typing import Any

import asyncio
from kivy.app import App
from kivymd.uix.snackbar import Snackbar

from config import Config, save_config
from utils import report_error, format_error, ErrorCode


class SettingsScreen:
    """Minimal settings screen for unit tests."""

    def __init__(self) -> None:
        app = App.get_running_app()
        self.kismet_field = SimpleNamespace(text=app.kismet_logdir)
        self.bcap_field = SimpleNamespace(text=app.bettercap_caplet)
        self.gps_poll_field = SimpleNamespace(text=str(app.map_poll_gps))
        self.gps_poll_max_field = SimpleNamespace(text=str(app.map_poll_gps_max))
        self.ap_poll_field = SimpleNamespace(text=str(app.map_poll_aps))
        self.bt_poll_field = SimpleNamespace(text=str(app.map_poll_bt))
        self.health_poll_field = SimpleNamespace(text=str(app.health_poll_interval))
        self.log_rotate_field = SimpleNamespace(text=str(app.log_rotate_interval))
        self.log_archives_field = SimpleNamespace(text=str(app.log_rotate_archives))
        self.cleanup_logs_switch = SimpleNamespace(active=app.cleanup_rotated_logs)
        self.offline_path_field = SimpleNamespace(text=app.offline_tile_path)
        self.offline_switch = SimpleNamespace(active=app.map_use_offline)
        self.auto_prefetch_switch = SimpleNamespace(active=app.map_auto_prefetch)
        self.show_gps_switch = SimpleNamespace(active=app.map_show_gps)
        self.show_aps_switch = SimpleNamespace(active=app.map_show_aps)
        self.show_bt_switch = SimpleNamespace(active=app.map_show_bt)
        self.cluster_switch = SimpleNamespace(active=app.map_cluster_aps)
        self.cluster_capacity_field = SimpleNamespace(
            text=str(app.map_cluster_capacity)
        )
        self.debug_switch = SimpleNamespace(active=app.debug_mode)
        self.battery_switch = SimpleNamespace(active=app.widget_battery_status)
        self.font_size_field = SimpleNamespace(text=str(app.ui_font_size))

    # ------------------------------------------------------------------
    def save_settings(self) -> None:  # pragma: no cover - exercised via tests
        app = App.get_running_app()
        if os.path.exists(self.kismet_field.text):
            app.kismet_logdir = self.kismet_field.text
        else:
            report_error("invalid path")

        if os.path.exists(self.bcap_field.text):
            app.bettercap_caplet = self.bcap_field.text
        else:
            report_error("invalid path")
        try:
            val = int(self.ap_poll_field.text)
            if val <= 0:
                raise ValueError
            app.map_poll_aps = val

            val = int(self.bt_poll_field.text)
            if val <= 0:
                raise ValueError
            app.map_poll_bt = val

            val = int(self.font_size_field.text)
            if val <= 0:
                raise ValueError
            app.ui_font_size = val

            val = int(self.health_poll_field.text)
            if val <= 0:
                raise ValueError
            app.health_poll_interval = val

            val = int(self.log_rotate_field.text)
            if val <= 0:
                raise ValueError
            app.log_rotate_interval = val

            val = int(self.log_archives_field.text)
            if val <= 0:
                raise ValueError
            app.log_rotate_archives = val

            app.cleanup_rotated_logs = self.cleanup_logs_switch.active

            val = int(self.gps_poll_field.text)
            if val <= 0:
                raise ValueError
            app.map_poll_gps = val

            val = int(self.gps_poll_max_field.text)
            if val <= 0:
                raise ValueError
            app.map_poll_gps_max = val

            val = int(self.cluster_capacity_field.text)
            if val <= 0:
                raise ValueError
            app.map_cluster_capacity = val
        except ValueError:
            report_error("GPS poll invalid")

        app.map_show_gps = self.show_gps_switch.active
        app.map_show_aps = self.show_aps_switch.active
        app.map_show_bt = self.show_bt_switch.active
        app.map_cluster_aps = self.cluster_switch.active
        app.map_auto_prefetch = self.auto_prefetch_switch.active
        app.debug_mode = self.debug_switch.active
        app.widget_battery_status = self.battery_switch.active

        if os.path.exists(self.offline_path_field.text):
            app.offline_tile_path = self.offline_path_field.text
        else:
            report_error("invalid path")

        cfg = app.config_data
        cfg.map_poll_aps = app.map_poll_aps
        cfg.map_poll_bt = app.map_poll_bt
        cfg.health_poll_interval = app.health_poll_interval
        cfg.log_rotate_interval = app.log_rotate_interval
        cfg.log_rotate_archives = app.log_rotate_archives
        cfg.cleanup_rotated_logs = app.cleanup_rotated_logs
        cfg.map_poll_gps = app.map_poll_gps
        cfg.map_poll_gps_max = app.map_poll_gps_max
        cfg.map_show_gps = app.map_show_gps
        cfg.map_show_aps = app.map_show_aps
        cfg.map_show_bt = app.map_show_bt
        cfg.map_cluster_aps = app.map_cluster_aps
        cfg.map_auto_prefetch = app.map_auto_prefetch
        cfg.map_cluster_capacity = app.map_cluster_capacity
        cfg.debug_mode = app.debug_mode
        cfg.widget_battery_status = app.widget_battery_status
        cfg.ui_font_size = app.ui_font_size
        cfg.offline_tile_path = app.offline_tile_path

        save_config(cfg)

    async def _export_logs(self) -> None:

        """Export application logs to a file and show notification."""
        app = App.get_running_app()
        path = await app.export_logs()
        if path:
            Snackbar(text=f"Exported {path}").open()

