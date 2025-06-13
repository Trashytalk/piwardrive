"""Screen displaying the interactive Wi-Fi/GPS map."""

import json
import os
import subprocess
import threading
import time

import requests
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapMarker, MapMarkerPopup, MBTilesMapSource, LineMapLayer
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextField


class MapScreen(Screen):  # pylint: disable=too-many-instance-attributes
    """Interactive map screen showing GPS location and AP overlays."""

    def __init__(self, **kwargs):
        """Initialize screen and marker storage."""
        super().__init__(**kwargs)
        self.gps_marker  = None
        self.ap_markers  = []
        self._gps_event  = None
        self._aps_event  = None
        self._lp_event   = None
        self.track_points = []
        self.track_layer = None

    def on_enter(self):  # pylint: disable=arguments-differ
        """Start GPS and AP polling when entering the screen."""
        app = App.get_running_app()
        if app.map_use_offline:
            try:
                self.ids.mapview.map_source = MBTilesMapSource('/mnt/ssd/tiles/offline.mbtiles')
            except Exception as e:
                Snackbar(text=f'Offline tiles error: {e}').open()
        self._gps_event = 'map_gps'
        self._aps_event = 'map_aps'
        app.scheduler.schedule(self._gps_event,
                               lambda dt: self.center_on_gps(),
                               app.map_poll_gps)
        app.scheduler.schedule(self._aps_event,
                               lambda dt: self.plot_aps(),
                               app.map_poll_aps)

    def on_leave(self):  # pylint: disable=arguments-differ
        """Unschedule polling tasks when leaving the screen."""
        app = App.get_running_app()
        if self._gps_event:
            app.scheduler.cancel(self._gps_event)
            self._gps_event = None
        if self._aps_event:
            app.scheduler.cancel(self._aps_event)
            self._aps_event = None
        if self._lp_event:
            Clock.unschedule(self._lp_event)
            self._lp_event = None

    # Long‐press detection scheduled on MapView
    def _map_touch_down(self, _mapview, touch):
        """Schedule long press detection."""
        if _mapview.collide_point(*touch.pos):
            self._lp_event = Clock.schedule_once(
                lambda dt: self._on_long_press(touch), 0.5
            )

    def _map_touch_move(self, _mapview, touch):
        """Cancel long press if the touch moves too far."""
        if self._lp_event and (abs(touch.dx) > dp(10) or abs(touch.dy) > dp(10)):
            Clock.unschedule(self._lp_event)
            self._lp_event = None

    def _map_touch_up(self, _mapview, touch):
        """Cancel pending long press on touch release."""
        if self._lp_event:
            Clock.unschedule(self._lp_event)
            self._lp_event = None

    def _on_long_press(self, touch):
        """Handle a confirmed long press gesture."""
        mv = self.ids.mapview
        lat, lon = mv.get_latlon_at(touch.x, touch.y)
        self._show_context_menu(lat, lon, touch.pos)

    def _show_context_menu(self, lat, lon, _pos):
        """Open a context menu for map actions at the given position."""
    items = [
            {"text": "Center here", "viewclass": "OneLineListItem",
             "on_release": lambda *a: (self.ids.mapview.center_on(lat, lon),
                                       self.context_menu.dismiss())},
            {"text": "Save this location", "viewclass": "OneLineListItem",
             "on_release": lambda *a: (self.save_waypoint(lat, lon), self.context_menu.dismiss())},
            {"text": "Load GPX Track", "viewclass": "OneLineListItem",
             "on_release": lambda *a: (self.load_gpx_prompt(), self.context_menu.dismiss())},
            {"text": "Measure distance", "viewclass": "OneLineListItem",
             "on_release": lambda *a: self._show_not_implemented("Measure distance")},
        ]
        self.context_menu = MDDropdownMenu(
            caller=self.ids.mapview,
            items=items,
            width_mult=3,
            max_height=dp(150)
        )
               self.context_menu.open()

    def save_waypoint(self, lat, lon):
        """Persist a waypoint to the user's config directory."""
        path = os.path.join(os.path.expanduser('~'), '.config', 'piwardrive', 'waypoints.json')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = []
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
        except Exception:
            data = []
        data.append({'lat': lat, 'lon': lon, 'ts': time.time()})
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, indent=2)
        Snackbar(text='Waypoint saved').open()

    def load_gpx_prompt(self):
        """Prompt the user for a GPX file path and load it."""
        self.gpx_field = MDTextField(hint_text='GPX file path', size_hint_x=.8,
                                     pos_hint={'center_x': .5, 'center_y': .6})
        self.gpx_dialog = MDDialog(title='Load GPX', type='custom',
                                   content_cls=self.gpx_field, buttons=[])
        self.gpx_dialog.open()
        self.gpx_field.bind(on_text_validate=lambda x: self._load_gpx(x.text))

    def _load_gpx(self, path):
        self.gpx_dialog.dismiss()
        try:
            points = []
            import xml.etree.ElementTree as ET
            tree = ET.parse(path)
            for trkpt in tree.findall('.//{*}trkpt'):
                lat = float(trkpt.get('lat'))
                lon = float(trkpt.get('lon'))
                points.append((lat, lon))
            if points:
                mv = self.ids.mapview
                layer = LineMapLayer(points=points)
                mv.add_layer(layer)
                Snackbar(text='Track loaded').open()
        except Exception as e:
            Snackbar(text=f'GPX load error: {e}').open()

    # GPS centering
    def center_on_gps(self):
        """Center the map on the current GPS location."""
        app = App.get_running_app()
        if not app.map_show_gps:
            return
        threading.Thread(target=self._fetch_and_center, daemon=True).start()

    def _fetch_and_center(self):
        """Fetch GPS coordinates in a thread and center the map."""
        try:
            proc = subprocess.run(
                ["gpspipe", "-w", "-n", "1"],
                capture_output=True, text=True, timeout=5
            )
            line = proc.stdout.strip().splitlines()[0]
            data = json.loads(line)
            lat, lon = data.get("lat"), data.get("lon")
            if lat is not None and lon is not None:
                self._update_map(lat, lon)
        except subprocess.TimeoutExpired:
            self._show_error("GPS lock timed out")
        except Exception as e:
            self._show_error(f"GPS error: {e}")

    @mainthread
    def _update_map(self, lat, lon):
        """Update map center and GPS marker from the main thread."""
        mv = self.ids.mapview
        mv.center_on(lat, lon)
        mv.zoom = 16

        # append to track and render polyline
        self.track_points.append((lat, lon))
        if len(self.track_points) > 1:
            if self.track_layer:
                mv.remove_layer(self.track_layer)
            self.track_layer = LineMapLayer(points=self.track_points)
            mv.add_layer(self.track_layer)

        if self.gps_marker:
            mv.remove_widget(self.gps_marker)
        if App.get_running_app().map_show_gps:
            self.gps_marker = MapMarker(
                lat=lat, lon=lon,
                source="widgets/center-icon.png",
                anchor_x="center", anchor_y="center"
            )
            mv.add_widget(self.gps_marker)

    # AP overlay
    def plot_aps(self):
        """Plot access point markers fetched from Kismet."""
        app = App.get_running_app()
        if not app.map_show_aps:
            return
        mv = self.ids.mapview
        for m in self.ap_markers:
            mv.remove_widget(m)
        self.ap_markers.clear()

        if app.map_cluster_aps:
            self._show_not_implemented("AP clustering")
            return

        try:
            resp = requests.get("http://127.0.0.1:2501/devices/all.json", timeout=5)
            for d in resp.json().get("devices", []):
                gps = d.get("gps-info")
                if gps and len(gps) >= 2:
                    m = MapMarkerPopup(
                        lat=gps[0], lon=gps[1],
                        source="widgets/marker-ap.png",
                        anchor_x="center", anchor_y="center"
                    )
                    m.add_widget(Label(
                        text=d.get("bssid", "AP"),
                        size_hint=(None, None),
                        size=(dp(80), dp(20))
                    ))
                    mv.add_widget(m)
                    self.ap_markers.append(m)
        except Exception as e:
            self._show_error(f"AP overlay error: {e}")

    # Layer menu
    def show_layer_menu(self, widget):
        """Display the layer toggle dropdown menu."""
        items = [
            {"text": "GPS Marker", "viewclass": "OneLineListItem",
             "on_release": lambda *a, k="map_show_gps": self._toggle(k)},
            {"text": "AP Markers", "viewclass": "OneLineListItem",
             "on_release": lambda *a, k="map_show_aps": self._toggle(k)},
            {"text": "BT Markers", "viewclass": "OneLineListItem",
             "on_release": lambda *a, k="map_show_bt": self._toggle(k)},
            {"text": "Cluster APs", "viewclass": "OneLineListItem",
             "on_release": lambda *a, k="map_cluster_aps": self._toggle(k)},
        ]
        self.layer_menu = MDDropdownMenu(caller=widget, items=items, width_mult=3)
        self.layer_menu.open()

    def _toggle(self, key):
        """Toggle a boolean App property and show feedback."""
        app = App.get_running_app()
        setattr(app, key, not getattr(app, key))
        self.layer_menu.dismiss()
        Snackbar(text=f"{key} = {getattr(app, key)}", duration=1.5).open()

    # Search / Jump to coords
    def open_search_dialog(self):
        """Open a dialog prompting for coordinates or an address."""
        self.search_field = MDTextField(
            hint_text="Lat,Lon or Address",
            pos_hint={"center_x": .5, "center_y": .6},
            size_hint_x=.8
        )
        self.search_dialog = MDDialog(
            title="Jump to…", type="custom",
            content_cls=self.search_field, buttons=[]
        )
        self.search_dialog.open()
        self.search_field.bind(
            on_text_validate=lambda x: self._perform_search(x.text)
        )

    def _perform_search(self, query):
        """Center map on the provided ``lat,lon`` query."""
        try:
            lat, lon = map(float, query.split(","))
        except:
            Snackbar(text="Invalid coords or geocode not implemented").open()
            return
        self.ids.mapview.center_on(lat, lon)
        self.ids.mapview.zoom = 16
        self.search_dialog.dismiss()

    # Screenshot
    def take_screenshot(self):
        """Save a PNG snapshot of the current map view."""
        fname = f"logs/map_{int(time.time())}.png"
        self.ids.mapview.export_to_png(fname)
        Snackbar(text=f"Saved {fname}").open()

    # Fullscreen
    def toggle_fullscreen(self):
        """Toggle fullscreen mode for the map."""
        app = App.get_running_app()
        app.map_fullscreen = not app.map_fullscreen
        root = app.root
        root.ids.nav_bar.opacity          = 0 if app.map_fullscreen else 1
        root.ids.diagnostics_bar.opacity  = 0 if app.map_fullscreen else 1
        root.ids.nav_bar.disabled         = app.map_fullscreen
        root.ids.diagnostics_bar.disabled = app.map_fullscreen

    # Help overlay
    def show_help_overlay(self):
        """Display usage instructions for the map view."""
        help_text = (
            "[b]Map Controls[/b]\n"
            "- Tap ⛶ to center on GPS\n"
            "- Tap +/– to zoom\n"
            "- Tap 🔍 to jump to coords\n"
            "- Tap 🖼 to snapshot\n"
            "- Tap 🗺️ to toggle layers\n"
            "- Long-press to open context menu\n"
        )
        MDDialog(title="Map Help", text=help_text, size_hint=(0.8, 0.6)).open()

    # Helpers
    def _show_error(self, msg):
        """Show an error message via ``Snackbar``."""
        Snackbar(text=msg, duration=3).open()

    def _show_not_implemented(self, feature_name):
        """Notify the user that a feature is not yet implemented."""
        Snackbar(text=f"{feature_name} not yet implemented", duration=2).open()
