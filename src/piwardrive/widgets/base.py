"""Base classes for dashboard widgets."""

from typing import Any

from piwardrive.simpleui import BoxLayout


class DashboardWidget(BoxLayout):
    """Simple widget container without GUI dependencies."""

    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def on_size(self, *_args: Any) -> None:  # pragma: no cover - no GUI
        """Handle resize events by updating child layout hints."""

        width = getattr(self, "width", 0)
        height = getattr(self, "height", 0)
        for child in self.children:
            if hasattr(child, "text_size"):
                child.text_size = (width, 0)
            if (
                hasattr(child, "size_hint_y")
                and child.size_hint_y is None
                and hasattr(child, "height")
            ):
                child.height = height
            if hasattr(child, "on_size") and child is not self:
                try:
                    child.on_size(*_args)
                except Exception:
                    pass
