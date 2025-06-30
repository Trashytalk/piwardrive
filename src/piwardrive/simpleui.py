"""Minimal UI shim used within the test suite.

This module provides very small stand-ins for a few Kivy widgets. They expose
just enough behaviour for the unit tests without pulling in the heavy Kivy
dependency.
"""

from __future__ import annotations

from typing import Any, Callable, Iterable


class Label:
    """Simple stand-in for ``kivy.uix.label.Label``."""

    def __init__(
        self,
        text: str = "",
        halign: str = "center",
        valign: str = "middle",
        **_kwargs: Any,
    ) -> None:
        """Initialize the label with optional text and alignment."""
        self.text: str = text
        self.halign: str = halign
        self.valign: str = valign
        self.text_size: tuple[int, int] = (0, 0)
        self.texture_size: list[int] = [0, 0]
        self.height: int = 0

    def bind(self, **_kwargs: Callable[[Any, Any], None]) -> None:
        """Bind callbacks to property changes (no-op in tests)."""
        pass


class Card:
    """Container widget that simply stores its children."""

    def __init__(
        self,
        orientation: str = "vertical",
        padding: int | float = 0,
        radius: Iterable[int] | None = None,
        **_kwargs: Any,
    ) -> None:
        """Create a new card layout container."""
        self.orientation: str = orientation
        self.padding: int | float = padding
        self.radius: list[int] = list(radius or [])
        self.children: list[Any] = []

    def add_widget(self, widget: Any) -> None:
        """Append ``widget`` to the list of children."""
        self.children.append(widget)


class BoxLayout:
    """Simplified vertical/horizontal layout container."""

    def __init__(self, **_kwargs: Any) -> None:
        """Create an empty layout."""
        self.children: list[Any] = []

    def add_widget(self, widget: Any) -> None:
        """Add ``widget`` to the container."""
        self.children.append(widget)

    def bind(self, **kwargs: Callable[[Any, Any], None]) -> None:
        """Immediately invoke provided callbacks (test helper)."""
        for cb in kwargs.values():
            cb(self, None)


class ScrollView:
    """Lightweight scroll view stub."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialise the view and store provided options."""
        self.width: int = 0
        self.children: list[Any] = []
        self.scroll_y: float = 0.0
        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_widget(self, widget: Any) -> None:
        """Append ``widget`` to the list of children."""
        self.children.append(widget)

    def bind(self, **kwargs: Callable[[Any, Any], None]) -> None:
        """Immediately invoke callbacks (test helper)."""
        for cb in kwargs.values():
            cb(self, None)


def dp(val: int | float) -> int | float:
    """Return ``val`` unchanged to mimic :func:`kivy.metrics.dp`."""
    return val


class Image:
    """Minimal image widget used in tests."""

    def __init__(self, **_kwargs: Any) -> None:
        """Initialise the image container."""
        self.source: str = ""
        self.size_hint_y: float | None = None
        self.height: int = 0

    def reload(self) -> None:
        """Reload the current image source (no-op)."""
        pass


class DropdownMenu:
    """Very small dropdown menu placeholder."""

    def __init__(self, **kwargs: Any) -> None:
        """Store provided ``kwargs`` for inspection by tests."""
        self.kwargs: dict[str, Any] = kwargs
        # Expose kwargs on the class for tests that inspect it
        type(self).kwargs = kwargs

    def open(self) -> None:
        """Open the menu (no-op in tests)."""
        pass

    def dismiss(self) -> None:
        """Close the menu (no-op in tests)."""
        pass
