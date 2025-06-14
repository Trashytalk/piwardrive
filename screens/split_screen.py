"""Screen showing map view alongside realtime capture statistics."""

# pylint: disable=line-too-long

from kivy.clock import Clock, mainthread
from kivy.uix.screenmanager import Screen


from utils import (
    fetch_metrics_async,
    get_avg_rssi,
    get_cpu_temp,
    get_gps_fix_quality,
    run_async_task,
    service_status,
)
from localization import _



class SplitScreen(Screen):
    """Display map on the left with metrics on the right."""
    def __init__(self, **kwargs):
        """Initialize widgets and schedule metric updates."""
        super().__init__(**kwargs)
        Clock.schedule_once(self._init_split, 0)
        Clock.schedule_interval(self._update_metrics, 2)


    def _init_split(self, _dt):
        """Perform the first metric update after creation."""
        self._update_metrics(0)

  
    @mainthread
    def _update_metrics(self, _dt):
        """Refresh labels with capture statistics."""
        cpu_temp = get_cpu_temp()

        def _apply(result: tuple[list, list, int]) -> None:
            aps, clients, handshake_count = result
            bssid_count = len(aps)
            avg_rssi = get_avg_rssi(aps)
            kismet_up = service_status('kismet')
            bettercap_up = service_status('bettercap')
            fix_quality = get_gps_fix_quality()

            self.ids.split_cpu_label.text              = (
                f"CPU: {cpu_temp:.1f}°C" if cpu_temp is not None else "CPU: N/A"
            )
            self.ids.split_bssid_label.text           = f"BSSIDs: {bssid_count}"
            self.ids.split_handshake_label.text       = f"Handshakes: {handshake_count}"
            self.ids.split_rssi_label.text            = (
                f"Avg RSSI: {avg_rssi:.1f} dBm" if avg_rssi is not None else "Avg RSSI: N/A"
            )
            self.ids.split_kismet_uptime_label.text    = f"Kismet: {'OK' if kismet_up else 'DOWN'}"
            self.ids.split_bettercap_uptime_label.text = f"BetterCAP: {'OK' if bettercap_up else 'DOWN'}"
            self.ids.split_fix_quality_label.text      = f"Fix: {fix_quality}"

        run_async_task(fetch_metrics_async(), _apply)

