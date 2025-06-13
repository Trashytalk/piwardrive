"""Scrollable widget that tails a log file."""

from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
import re
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from utils import tail_file


class LogViewer(ScrollView):
    """Display the last N lines of a log file and update periodically."""

    log_path = StringProperty("/var/log/syslog")
    max_lines = NumericProperty(200)
    poll_interval = NumericProperty(1.0)
    filter_regex = StringProperty("")
    error_regex = StringProperty("error")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(size_hint_y=None, halign="left", valign="top")
        self.label.bind(texture_size=self._update_height)
        self.add_widget(self.label)
        self.bind(width=self._update_text_size)
        self._filter_re = None
        self._error_re = re.compile(self.error_regex, re.IGNORECASE)
        self.bind(filter_regex=self._compile_filter)
        self.bind(error_regex=self._compile_error)
        Clock.schedule_interval(self._refresh, self.poll_interval)

    
    def _compile_filter(self, *_args):
        self._filter_re = (
            re.compile(self.filter_regex)
            if self.filter_regex
            else None
        )

    def _compile_error(self, *_args):
        self._error_re = re.compile(self.error_regex, re.IGNORECASE)

    def _update_text_size(self, _instance, _value):
        self.label.text_size = (self.width, None)

    def _update_height(self, _instance, _value):
        self.label.height = self.label.texture_size[1]
        # keep scrolled to bottom after update
        self.scroll_y = 0

    def _refresh(self, _dt):
        lines = tail_file(self.log_path, self.max_lines)
        if self._filter_re:
            try:
                lines = [ln for ln in lines if self._filter_re.search(ln)]
            except re.error:
                pass
        self.label.text = "\n".join(lines)
        
    def jump_to_latest_error(self):
        """Scroll to the most recent line matching ``error_regex``."""
        if not self._error_re:
            return
        lines = self.label.text.splitlines()
        for idx in range(len(lines) - 1, -1, -1):
            if self._error_re.search(lines[idx]):
                if len(lines) > 1:
                    self.scroll_y = 1 - idx / max(len(lines) - 1, 1)
                else:
                    self.scroll_y = 1
                break
