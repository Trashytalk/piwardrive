import logging


try:  # pragma: no cover - optional GUI dependency
    import tkinter as _tk
    from tkinter import messagebox as _messagebox
except Exception:  # pragma: no cover - headless or tkinter missing
    _tk = None  # type: ignore[assignment]
    _messagebox = None  # type: ignore[assignment]

_tk_root: object | None = None


def _get_root() -> object | None:
    """Return a hidden ``Tk`` instance or ``None`` when not available."""

    global _tk_root
    if _tk is None:
        return None
    if _tk_root is None:
        try:  # pragma: no cover - may fail on headless systems
            _tk_root = _tk.Tk()
            _tk_root.withdraw()
        except Exception:
            _tk_root = None
    return _tk_root


class App:
    """Minimal application helper that tracks a running instance."""

    _instance: "App | None" = None

    def __init__(self) -> None:
        self._root = _get_root()
        App._instance = self

    @staticmethod
    def get_running_app() -> "App | None":
        """Return the current application instance if one exists."""

        return App._instance

    def show_alert(self, title: str, message: str) -> None:
        """Display ``message`` in a simple popup when possible."""

        if _messagebox is None:
            return
        root = self._root if self._root is not None else _get_root()
        if root is None:
            return
        try:  # pragma: no cover - UI update
            _messagebox.showerror(title, message, parent=root)  # type: ignore[arg-type]
        except Exception:
            pass


ERROR_PREFIX = "E"


def format_error(code: int, message: str) -> str:
    """Return standardized error string like ``[E001] message``."""
    return f"[{ERROR_PREFIX}{int(code):03d}] {message}"


def report_error(message: str) -> None:
    """Log the error."""
    logging.error(message)
    try:
        app = App.get_running_app()
        if app and hasattr(app, "show_alert"):
            app.show_alert("Error", message)
    except Exception as exc:  # pragma: no cover - app may not be running
        logging.exception("Failed to display error alert: %s", exc)


__all__ = ["ERROR_PREFIX", "format_error", "report_error"]
