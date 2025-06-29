"""Scrollable widget that tails a log file."""

import os
import re
from typing import Any, List

try:  # pragma: no cover - prefer real KivyMD menu if available
    from kivymd.uix.menu import MDDropdownMenu
except Exception:  # pragma: no cover - fallback stub
    from piwardrive.simpleui import DropdownMenu as MDDropdownMenu
from piwardrive.simpleui import Label, ScrollView
try:  # pragma: no cover - optional App stub for tests
    from piwardrive.simpleui import App  # type: ignore
except Exception:  # pragma: no cover - fallback when missing
    class App:
        @staticmethod
        def get_running_app() -> None:
            return None
from piwardrive.utils import tail_file


class LogViewer(ScrollView):
    """Display the last N lines of a log file and update periodically."""

    log_path: str = "/var/log/syslog"
    max_lines: int = 200
    poll_interval: float = 1.0
    filter_regex: str = ""
    error_regex: str = "error"
    log_paths: List[str] = []

    def __init__(self, **kwargs: Any) -> None:
        """Set up label widget and schedule periodic log refresh."""
        super().__init__(**kwargs)
        self.label = Label(size_hint_y=None, halign="left", valign="top")
        self.label.bind(texture_size=self._update_height)
        self.add_widget(self.label)
        self.bind(width=self._update_text_size)
        self._filter_re: re.Pattern[str] | None = None
        self._error_re: re.Pattern[str] = re.compile(self.error_regex, re.IGNORECASE)
        self.bind(filter_regex=self._compile_filter)
        self.bind(error_regex=self._compile_error)
        self.log_paths = [self.log_path]
        self._menu: MDDropdownMenu | None = None

    def _compile_filter(self, *_args: Any) -> None:
        self._filter_re = re.compile(self.filter_regex) if self.filter_regex else None

    def _compile_error(self, *_args: Any) -> None:
        self._error_re = re.compile(self.error_regex, re.IGNORECASE)

    def _update_text_size(self, _instance: Any, _value: Any) -> None:
        self.label.text_size = (self.width, 0)

    def _update_height(self, _instance: Any, _value: Any) -> None:
        self.label.height = self.label.texture_size[1]
        # keep scrolled to bottom after update
        self.scroll_y = 0.0

    def _refresh(self, _dt: float) -> None:
        lines = tail_file(self.log_path, self.max_lines)
        if self._filter_re:
            try:
                lines = [ln for ln in lines if self._filter_re.search(ln)]
            except re.error:
                pass
        self.label.text = "\n".join(lines)

    def jump_to_latest_error(self) -> None:
        """Scroll to the most recent line matching ``error_regex``."""
        if not self._error_re:
            return
        lines = self.label.text.splitlines()
        for idx in range(len(lines) - 1, -1, -1):
            if self._error_re.search(lines[idx]):
                if len(lines) > 1:
                    self.scroll_y = 1.0 - idx / max(len(lines) - 1, 1)
                else:
                    self.scroll_y = 1
                break

    def show_path_menu(self, caller: Any) -> None:  # pragma: no cover - GUI
        """Display a dropdown menu to select ``log_path``."""
        items = [
            {
                "text": os.path.basename(p),
                "viewclass": "OneLineListItem",
                "on_release": lambda p=p: self._select_path(p),
            }
            for p in self.log_paths
        ]
        self._menu = MDDropdownMenu(caller=caller, items=items, width_mult=4)
        self._menu.open()

    def _select_path(self, path: str) -> None:
        """Update ``log_path`` and close the menu."""
        self.log_path = path
        if self._menu:
            self._menu.dismiss()
