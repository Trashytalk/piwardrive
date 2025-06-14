"""Base classes for dashboard widgets with drag-and-drop support."""

from typing import Any

from kivy.uix.behaviors import DragBehavior
from kivymd.uix.boxlayout import MDBoxLayout


class DashboardWidget(DragBehavior, MDBoxLayout):
    """Simple draggable widget container."""

    update_interval = 5.0
    
    def __init__(self, **kwargs: Any) -> None:
        """Initialize draggable widget container."""
        super().__init__(**kwargs)
        self.drag_rectangle = self.x, self.y, self.width, self.height
        self.drag_timeout = 10000000
        self.drag_distance = 0

    def on_size(self, *args: Any) -> None:
        """Update drag area when the widget size changes."""
        self.drag_rectangle = self.x, self.y, self.width, self.height
