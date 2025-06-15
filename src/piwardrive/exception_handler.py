import logging
from kivy.base import ExceptionHandler, ExceptionManager


class LogExceptionHandler(ExceptionHandler):
    """Logs uncaught Kivy exceptions to the application log."""

    def handle_exception(self, inst):
        logging.exception(
            "Unhandled exception",
            exc_info=(type(inst), inst, inst.__traceback__),
        )
        return ExceptionManager.PASS


def install():
    """Register the log exception handler with Kivy."""
    ExceptionManager.add_handler(LogExceptionHandler())
