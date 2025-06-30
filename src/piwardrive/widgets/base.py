"""Base classes for dashboard widgets."""

from typing import Any

from piwardrive.ui import BoxLayout


class DashboardWidget(BoxLayout):
    """Simple widget container without GUI dependencies."""

    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def on_size(self, *_args: Any) -> None:  # pragma: no cover - no GUI
        pass
