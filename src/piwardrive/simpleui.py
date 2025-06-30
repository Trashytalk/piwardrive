"""Minimal UI shim used within the test suite.

This module provides very small stand-ins for a few Kivy widgets. They expose
just enough behaviour for the unit tests without pulling in the heavy Kivy
dependency.
"""

from __future__ import annotations

from typing import Any, Callable, Iterable

# Attempt to import tkinter for basic GUI support.  When unavailable or a display
# cannot be opened, ``tk`` will remain ``None`` and all widgets fall back to the
# previous no-op behaviour used in the tests.
try:  # pragma: no cover - optional dependency
    import tkinter as tk
except Exception:  # pragma: no cover - running headless or tkinter missing
    tk = None  # type: ignore[assignment]

_tk_root: Any | None = None


def _get_root() -> Any | None:
    """Return a hidden ``Tk`` instance or ``None`` when not available."""

    global _tk_root
    if tk is None:
        return None
    if _tk_root is None:
        try:  # pragma: no cover - may fail on headless systems
            _tk_root = tk.Tk()
            _tk_root.withdraw()
        except Exception:
            _tk_root = None
    return _tk_root


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
        self._callbacks: dict[str, list[Callable[[Any, Any], None]]] = {}
        self._widget: Any | None = None
        self.text: str = text
        self.halign: str = halign
        self.valign: str = valign
        self.text_size: tuple[int, int] = (0, 0)
        self.texture_size: list[int] = [0, 0]
        self.height: int = 0

        root = _get_root()
        if root is not None:
            try:  # pragma: no cover - UI update
                justify = {
                    "left": tk.LEFT,
                    "center": tk.CENTER,
                    "right": tk.RIGHT,
                }.get(halign, tk.LEFT)
                self._widget = tk.Label(root, text=text, justify=justify)
                self._widget.pack()
                self._widget.update_idletasks()
                self.texture_size = [
                    self._widget.winfo_reqwidth(),
                    self._widget.winfo_reqheight(),
                ]
            except Exception:
                self._widget = None

    def __setattr__(self, name: str, value: Any) -> None:
        object.__setattr__(self, name, value)
        if name == "text":  # update underlying widget
            widget = getattr(self, "_widget", None)
            if widget is not None:
                try:  # pragma: no cover - GUI update
                    widget.config(text=value)
                    widget.update_idletasks()
                    width = widget.winfo_reqwidth()
                    height = widget.winfo_reqheight()
                    object.__setattr__(self, "texture_size", [width, height])
                    for cb in self._callbacks.get("texture_size", []):
                        cb(self, self.texture_size)
                except Exception:
                    pass
        if name in getattr(self, "_callbacks", {}):
            for cb in self._callbacks[name]:
                cb(self, value)

    def bind(self, **kwargs: Callable[[Any, Any], None]) -> None:
        """Attach callbacks to property changes."""
        for prop, cb in kwargs.items():
            self._callbacks.setdefault(prop, []).append(cb)


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
        self._widget: Any | None = None

    def reload(self) -> None:
        """Reload the current image source if ``tkinter`` is available."""
        if tk is None:
            return
        root = _get_root()
        if root is None or not self.source:
            return
        try:  # pragma: no cover - GUI update
            img = tk.PhotoImage(file=self.source)
        except Exception:
            return
        if self._widget is None:
            try:
                self._widget = tk.Label(root, image=img)
                self._widget.image = img
                self._widget.pack()
            except Exception:
                self._widget = None
                return
        else:
            try:
                self._widget.configure(image=img)
                self._widget.image = img
            except Exception:
                return
        try:
            root.update_idletasks()
        except Exception:
            pass


class DropdownMenu:
    """Very small dropdown menu placeholder."""

    def __init__(self, **kwargs: Any) -> None:
        """Store provided ``kwargs`` for inspection by tests."""
        self.kwargs: dict[str, Any] = kwargs
        # Expose kwargs on the class for tests that inspect it
        type(self).kwargs = kwargs
        self._window: Any | None = None

    def open(self) -> None:
        """Open the menu using ``tkinter`` if available."""
        if tk is None:
            return
        root = _get_root()
        if root is None:
            return
        try:  # pragma: no cover - GUI update
            self._window = tk.Toplevel(root)
            for item in self.kwargs.get("items", []):
                text = item.get("text", "")
                cmd = item.get("on_release")
                tk.Button(self._window, text=text, command=cmd).pack(fill=tk.X)
            self._window.update_idletasks()
        except Exception:
            self._window = None

    def dismiss(self) -> None:
        """Close the menu if it was opened."""
        if self._window is not None:
            try:  # pragma: no cover - GUI update
                self._window.destroy()
            except Exception:
                pass
            finally:
                self._window = None
