"""Scrollable widget that tails a log file."""

from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from utils import tail_file


class LogViewer(ScrollView):
    """Display the last N lines of a log file and update periodically."""

    log_path = StringProperty("/var/log/syslog")
    max_lines = NumericProperty(200)
    poll_interval = NumericProperty(1.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(size_hint_y=None, halign="left", valign="top")
        self.label.bind(texture_size=self._update_height)
        self.add_widget(self.label)
        self.bind(width=self._update_text_size)
        Clock.schedule_interval(self._refresh, self.poll_interval)

    def _update_text_size(self, _instance, _value):
        self.label.text_size = (self.width, None)

    def _update_height(self, _instance, _value):
        self.label.height = self.label.texture_size[1]
        # keep scrolled to bottom after update
        self.scroll_y = 0

    def _refresh(self, _dt):
        lines = tail_file(self.log_path, self.max_lines)
        self.label.text = "\n".join(lines)
        
