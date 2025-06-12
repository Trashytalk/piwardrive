from kivy.uix.screenmanager import Screen
from kivy.clock import Clock, mainthread
from kivy.app import App

from utils import (
    get_cpu_temp,
    fetch_kismet_devices,
    count_bettercap_handshakes,
    # avg RSSI helper: average over access_points[*]['signal_dbm']
    # implement get_avg_rssi in utils
    get_avg_rssi,
    # service status helper returns bool
    service_status,
    # GPS fix quality helper: returns 2D/3D/DGPS
    get_gps_fix_quality,
)

class SplitScreen(Screen):
    """
    A split-screen view showing the Map on the left with a border,
    and key metrics on the right locked to 1/3 width.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._init_split, 0)
        Clock.schedule_interval(self._update_metrics, 2)

    def _init_split(self, dt):
        # initial metric update
        self._update_metrics(0)

    @mainthread
    def _update_metrics(self, dt):
        cpu_temp = get_cpu_temp()
        aps, clients = fetch_kismet_devices()
        bssid_count = len(aps)
        handshake_count = count_bettercap_handshakes()
        avg_rssi = get_avg_rssi(aps)
        kismet_up = service_status('kismet')
        bettercap_up = service_status('bettercap')
        fix_quality = get_gps_fix_quality()

        self.ids.split_cpu_label.text              = f"CPU: {cpu_temp:.1f}°C" if cpu_temp is not None else "CPU: N/A"
        self.ids.split_bssid_label.text           = f"BSSIDs: {bssid_count}"
        self.ids.split_handshake_label.text       = f"Handshakes: {handshake_count}"
        self.ids.split_rssi_label.text            = f"Avg RSSI: {avg_rssi:.1f} dBm" if avg_rssi is not None else "Avg RSSI: N/A"
        self.ids.split_kismet_uptime_label.text    = f"Kismet: {'OK' if kismet_up else 'DOWN'}"
        self.ids.split_bettercap_uptime_label.text = f"BetterCAP: {'OK' if bettercap_up else 'DOWN'}"
        self.ids.split_fix_quality_label.text      = f"Fix: {fix_quality}"
