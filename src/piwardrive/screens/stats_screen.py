"""System statistics screen for CPU, memory and disk usage."""

import psutil

from kivy.app import App
from kivy.uix.screenmanager import Screen
from piwardrive.utils import (
    get_cpu_temp,
    get_smart_status,
    require_id,
    service_status,
)
from piwardrive.localization import _


class StatsScreen(Screen):
    """Display basic system metrics in the diagnostics bar."""

    def __init__(self, **kwargs):
        """Schedule periodic stat updates."""
        super().__init__(**kwargs)
        App.get_running_app().scheduler.schedule(
            "stats_update", lambda dt: self.update_stats(dt), 2
        )


    def update_stats(self, _dt):
        """Refresh temperature, memory and disk usage labels."""
        # compute metrics
        app = App.get_running_app()
        monitor = getattr(app, "health_monitor", None)
        data = monitor.data if monitor else None

        if data:
            system = data.get("system", {})
            cpu_temp = system.get("cpu_temp")
            mem_pct = system.get("memory_percent")
            disk_pct = system.get("disk_percent")
            smart = system.get("ssd_smart")
            services = data.get("services", {})
        else:
            cpu_temp = get_cpu_temp()
            mem_pct = psutil.virtual_memory().percent if psutil else None
            disk_pct = psutil.disk_usage('/mnt/ssd').percent if psutil else None
            smart = get_smart_status('/mnt/ssd')
            services = {
                "kismet": service_status("kismet"),
                "bettercap": service_status("bettercap"),
            }


        # fetch root diagnostics bar labels
        root = App.get_running_app().root
        cpu_lbl = require_id(root, "cpu_label")
        mem_lbl = require_id(root, "mem_label")
        disk_lbl = require_id(root, "disk_label")

        if 'disk_health_label' in self.ids:
            health_lbl = self.ids.disk_health_label
        else:
            health_lbl = None


        # update text
        cpu_lbl.text  = (
            f"{_('cpu')}: {cpu_temp:.1f}°C" if cpu_temp is not None else f"{_('cpu')}: {_('not_available')}"
        )
        mem_lbl.text  = (
            f"{_('mem')}: {mem_pct:.0f}%" if mem_pct is not None else f"{_('mem')}: {_('not_available')}"
        )
        disk_lbl.text = (
            f"{_('ssd')}: {disk_pct:.0f}%" if disk_pct is not None else f"{_('ssd')}: {_('not_available')}"
        )
        if health_lbl is not None:
            health_lbl.text = (
                f"{_('ssd_health')}: {smart}" if smart else f"{_('ssd_health')}: {_('not_available')}"
            )

        if 'kismet_status_label' in self.ids:
            status = services.get('kismet')
            self.ids.kismet_status_label.text = (
                f"{_('kismet')}: {(_('ok') if status else _('down'))}"
                if status is not None
                else f"{_('kismet')}: {_('not_available')}"
            )
        if 'bettercap_status_label' in self.ids:
            status = services.get('bettercap')
            self.ids.bettercap_status_label.text = (
                f"{_('bettercap')}: {(_('ok') if status else _('down'))}"
                if status is not None
                else f"{_('bettercap')}: {_('not_available')}"
            )
