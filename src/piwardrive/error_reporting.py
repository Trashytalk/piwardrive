import logging

try:
    from kivy.app import App as KivyApp
except Exception:  # pragma: no cover - optional dependency
    KivyApp = None  # type: ignore[assignment]

App = KivyApp


ERROR_PREFIX = "E"


def format_error(code: int, message: str) -> str:
    """Return standardized error string like ``[E001] message``."""
    return f"[{ERROR_PREFIX}{int(code):03d}] {message}"


def report_error(message: str) -> None:
    """Log the error."""
    logging.error(message)
    try:
        app = App.get_running_app() if App is not None else None
        if app and hasattr(app, "show_alert"):
            app.show_alert("Error", message)
    except Exception as exc:  # pragma: no cover - app may not be running
        logging.exception("Failed to display error alert: %s", exc)



__all__ = ["ERROR_PREFIX", "format_error", "report_error"]
