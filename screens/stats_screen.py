## stats_screen

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.app import App
import psutil
from utils import get_cpu_temp

class StatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_stats, 2)

    def update_stats(self, dt):
        # compute metrics
        cpu_temp = get_cpu_temp()
        mem_pct  = psutil.virtual_memory().percent if psutil else None
        disk_pct = psutil.disk_usage('/mnt/ssd').percent if psutil else None

        # fetch root diagnostics bar labels
        root = App.get_running_app().root
        cpu_lbl  = root.ids.cpu_label
        mem_lbl  = root.ids.mem_label
        disk_lbl = root.ids.disk_label

        # update text
        cpu_lbl.text  = f"CPU: {cpu_temp:.1f}°C" if cpu_temp is not None else "CPU: N/A"
        mem_lbl.text  = f"Mem: {mem_pct:.0f}%"    if mem_pct  is not None else "Mem: N/A"
        disk_lbl.text = f"SSD: {disk_pct:.0f}%"   if disk_pct is not None else "SSD: N/A"
