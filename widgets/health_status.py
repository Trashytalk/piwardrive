import logging
from typing import Any

from kivy.app import App
from kivymd.uix.label import MDLabel

from .base import DashboardWidget


class HealthStatusWidget(DashboardWidget):
    """Display results from the global health monitor."""

    update_interval = 10.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.label = MDLabel(text="Health: N/A")
        self.add_widget(self.label)
        self.update()

    def update(self) -> None:  # pragma: no cover - GUI update
        try:
            app = App.get_running_app()
            monitor = getattr(app, "health_monitor", None)
            data = monitor.data if monitor else None
            if not data:
                self.label.text = "Health: N/A"
                return
            disk = data["system"]["disk_percent"]
            net = "OK" if data["network_ok"] else "DOWN"
            services = " ".join(
                f"{name}:{'OK' if ok else 'DOWN'}" for name, ok in data["services"].items()
            )
            self.label.text = f"Net:{net} SSD:{disk:.0f}% {services}"
        except Exception as exc:
            logging.exception("HealthStatusWidget update failed: %s", exc)
