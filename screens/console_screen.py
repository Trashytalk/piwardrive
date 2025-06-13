+14-14
"""Simple screen hosting a console log view."""␊
␊
from kivy.uix.screenmanager import Screen␊
␊
from widgets import LogViewer␊
␊
␊
class ConsoleScreen(Screen):␊
    """Display real-time logs from Kismet or other services."""␊
␊
    def __init__(self, **kwargs):␊
        super().__init__(**kwargs)␊
        self.log_widget = LogViewer()␊
        self.add_widget(self.log_widget)␊
