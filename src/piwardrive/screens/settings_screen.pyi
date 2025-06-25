from __future__ import annotations

from typing import Any

from kivy.uix.screenmanager import Screen


class SettingsScreen(Screen):
    kismet_field: Any
    bcap_field: Any
    gps_poll_field: Any
    gps_poll_max_field: Any
    ap_poll_field: Any
    bt_poll_field: Any
    health_poll_field: Any
    log_rotate_field: Any
    log_archives_field: Any
    offline_path_field: Any
    tile_maint_field: Any
    route_prefetch_field: Any
    theme_field: Any
    offline_switch: Any
    show_gps_switch: Any
    show_aps_switch: Any
    show_bt_switch: Any
    cluster_switch: Any
    cluster_capacity_field: Any
    debug_switch: Any
    battery_switch: Any
    font_size_field: Any

    def on_enter(self) -> None: ...
    def save_settings(self) -> None: ...
