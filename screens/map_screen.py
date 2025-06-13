"""Screen displaying the interactive Wi-Fi/GPS map."""



import json

import os

import subprocess

import threading
import time

import requests
import pandas as pd
import math
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

from utils import haversine_distance, polygon_area




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
        self.ruler_points = []
        self.area_points = []
        self.breadcrumb = []
        self._compass_heading = 0.0


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

@@ -67,70 +75,70 @@ class MapScreen(Screen): # pylint: disable=too-many-instance-attributes
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



    def _show_context_menu(self, lat, lon, _pos):␊
        """Open a context menu for map actions at the given position."""␊
        items = [
            {"text": "Center here", "viewclass": "OneLineListItem",␊
             "on_release": lambda *a: (self.ids.mapview.center_on(lat, lon),␊
                                       self.context_menu.dismiss())},␊
            {"text": "Save this location", "viewclass": "OneLineListItem",␊
             "on_release": lambda *a: (self.save_waypoint(lat, lon), self.context_menu.dismiss())},␊
            {"text": "Load GPX Track", "viewclass": "OneLineListItem",␊
             "on_release": lambda *a: (self.load_gpx_prompt(), self.context_menu.dismiss())},␊
            {"text": "Measure distance", "viewclass": "OneLineListItem",␊
             "on_release": lambda *a: self.start_ruler_mode()},
        ]␊
        self.context_menu = MDDropdownMenu(␊
            caller=self.ids.mapview,␊
            items=items,␊
            width_mult=3,␊
            max_height=dp(150)␊
        )␊
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



@@ -195,69 +203,74 @@ class MapScreen(Screen): # pylint: disable=too-many-instance-attributes
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
                    m.ap_data = {
                        "bssid": d.get("bssid"),
                        "ssid": d.get("ssid"),
                        "encryption": d.get("encryption"),
                    }
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

@@ -303,28 +316,199 @@ class MapScreen(Screen): # pylint: disable=too-many-instance-attributes
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

    # ------------------------------------------------------------------
    # Distance & Area Measurement Tools
    def start_ruler_mode(self):
        """Activate ruler mode for measuring distance between two taps."""
        self.ruler_points.clear()
        Snackbar(text="Ruler mode: tap two points").open()

    def add_ruler_point(self, lat, lon):
        """Record a point for ruler mode and display the distance when two are set."""
        self.ruler_points.append((lat, lon))
        if len(self.ruler_points) == 2:
            dist = haversine_distance(self.ruler_points[0], self.ruler_points[1])
            Snackbar(text=f"Distance: {dist:.1f} m").open()
            self.ruler_points.clear()

    def start_area_mode(self):
        """Begin polygon drawing for area calculation."""
        self.area_points.clear()
        Snackbar(text="Area mode: tap points then long‑press to finish").open()

    def add_area_point(self, lat, lon):
        """Add a vertex to the current area polygon."""
        self.area_points.append((lat, lon))

    def finish_area_mode(self):
        """Compute and display the polygon area."""
        area = polygon_area(self.area_points)
        Snackbar(text=f"Area: {area:.1f} m²").open()
        self.area_points.clear()

    # ------------------------------------------------------------------
    # Offline Map Tile Management
    def prefetch_tiles(self, bounds, zoom=16):
        """Download MBTiles covering ``bounds`` (min_lat, min_lon, max_lat, max_lon)."""
        try:
            # Placeholder implementation
            _ = bounds, zoom
        except Exception as e:
            self._show_error(f"Prefetch error: {e}")

    def purge_old_tiles(self, max_age_days=30, folder='/mnt/ssd/tiles'):
        """Delete cached tiles older than ``max_age_days`` days."""
        cutoff = time.time() - max_age_days * 86400
        try:
            for root, _, files in os.walk(folder):
                for f in files:
                    path = os.path.join(root, f)
                    if os.path.getmtime(path) < cutoff:
                        os.remove(path)
        except Exception as e:
            self._show_error(f"Tile purge error: {e}")

    def enforce_cache_limit(self, folder='/mnt/ssd/tiles', limit_mb=512):
        """Ensure tile cache does not exceed ``limit_mb`` megabytes."""
        try:
            files = []
            total = 0
            for root, _, fns in os.walk(folder):
                for fn in fns:
                    path = os.path.join(root, fn)
                    size = os.path.getsize(path)
                    total += size
                    files.append((path, size))
            max_bytes = limit_mb * 1024 * 1024
            if total <= max_bytes:
                return
            files.sort(key=lambda x: os.path.getmtime(x[0]))
            for path, size in files:
                os.remove(path)
                total -= size
                if total <= max_bytes:
                    break
        except Exception as e:
            self._show_error(f"Cache limit error: {e}")

    # ------------------------------------------------------------------
    # Thematic Layers & Filtering
    def filter_ap_markers(self, ssid=None, encryption=None, oui=None):
        """Filter AP markers based on SSID, encryption type, or MAC OUI."""
        for m in self.ap_markers:
            data = getattr(m, 'ap_data', {})
            visible = True
            if ssid and ssid not in (data.get('ssid') or ''):
                visible = False
            if encryption and encryption != data.get('encryption'):
                visible = False
            if oui and not (data.get('bssid') or '').startswith(oui):
                visible = False
            m.opacity = 1 if visible else 0

    def apply_icon_set(self, icon_map):
        """Update AP marker icons according to ``icon_map`` keyed by encryption."""
        for m in self.ap_markers:
            data = getattr(m, 'ap_data', {})
            enc = data.get('encryption')
            if enc in icon_map:
                m.source = icon_map[enc]

    # ------------------------------------------------------------------
    # Map Orientation & Sensors
    def update_compass(self, heading):
        """Rotate map view to match the given compass ``heading``."""
        self._compass_heading = heading
        self.ids.mapview.rotation = -heading

    def update_tilt(self, pitch, roll):
        """Placeholder for pitch/roll 3D tilt effect."""
        _ = pitch, roll  # not implemented

    def register_sensor(self, name, handler):
        """Store additional sensor handler for future use."""
        setattr(self, f'sensor_{name}', handler)

    # ------------------------------------------------------------------
    # Routing & Navigation Aids
    def show_turn_prompt(self, message):
        """Display a navigation prompt."""
        MDDialog(title="Navigation", text=message, buttons=[]).open()

    def breadcrumb_path(self):
        """Return a reversed list of track points for backtracking."""
        return list(reversed(self.track_points))

    # ------------------------------------------------------------------
    # Export & Sharing
    def export_points_csv(self, path):
        """Dump discovered AP locations to ``path`` as CSV."""
        data = [getattr(m, 'ap_data', {}) for m in self.ap_markers]
        try:
            pd.DataFrame(data).to_csv(path, index=False)
            Snackbar(text=f"Exported {path}").open()
        except Exception as e:
            self._show_error(f"Export error: {e}")

    def create_pdf_snapshot(self, path):
        """Generate a PDF of the current map view."""
        png_path = f"{path}.png"
        self.ids.mapview.export_to_png(png_path)
        try:
            import img2pdf
            with open(path, 'wb') as fh:
                fh.write(img2pdf.convert(png_path))
            os.remove(png_path)
            Snackbar(text=f"Saved {path}").open()
        except Exception as e:
            self._show_error(f"PDF export error: {e}")

    # ------------------------------------------------------------------
    # Clustering Behaviors
    def update_clusters_on_zoom(self, zoom):
        """Placeholder to re-cluster AP markers based on ``zoom`` level."""
        _ = zoom

    def spiderfy_markers(self):
        """Placeholder to spread overlapping markers."""
        pass

    def adjust_quadtree(self, capacity):
        """Placeholder for quadtree parameter adjustment."""
        _ = capacity

    # ------------------------------------------------------------------
    # Custom Marker Styles
    def update_marker_icons(self, icon_map):
        """Apply icons based on encryption type using ``icon_map`` mapping."""
        self.apply_icon_set(icon_map)

    def set_directional_marker(self, marker, bearing):
        """Rotate ``marker`` to indicate relative ``bearing``."""
        marker.rotation = bearing
