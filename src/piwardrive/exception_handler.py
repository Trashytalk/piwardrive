"""Helpers for capturing uncaught exceptions."""
import logging
from kivy.base import ExceptionHandler, ExceptionManager


_installed = False


class LogExceptionHandler(ExceptionHandler):
    """Logs uncaught Kivy exceptions to the application log."""

    def handle_exception(self, inst):
        """Log the exception and let Kivy continue processing."""
        logging.exception(
            "Unhandled exception",
            exc_info=(type(inst), inst, inst.__traceback__),
        )
        return ExceptionManager.PASS


def install():
    """Register the log exception handler with Kivy."""
    global _installed
    if _installed:
        return
    for h in ExceptionManager.handlers:
        if isinstance(h, LogExceptionHandler):
            _installed = True
            return
    ExceptionManager.add_handler(LogExceptionHandler())
    _installed = True
