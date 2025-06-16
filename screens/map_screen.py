"""Screen displaying the interactive Wi-Fi/GPS map."""



import json
import os
import asyncio
import aiohttp


from gpsd_client import client as gps_client


import threading

import time



import gps
import requests
from typing import Callable

import csv

import math
import asyncio

from kivy.app import App
import utils

from kivy.clock import Clock, mainthread
from kivy.animation import Animation

from kivy.metrics import dp



from kivy.uix.label import Label

from kivy.uix.screenmanager import Screen

from kivy_garden.mapview import (

    MapMarker,

    MapMarkerPopup,

    MBTilesMapSource,

    LineMapLayer,

)

from kivymd.uix.dialog import MDDialog

from kivymd.uix.menu import MDDropdownMenu

from kivymd.uix.snackbar import Snackbar
from persistence import save_app_state
from kivymd.uix.textfield import MDTextField
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
import export
from utils import (
    haversine_distance,
    polygon_area,
    load_kml,
    point_in_polygon,
    report_error,
)




class MapScreen(Screen):  # pylint: disable=too-many-instance-attributes

    """Interactive map screen showing GPS location and AP overlays."""



    def __init__(self, **kwargs):

        """Initialize screen and marker storage."""

        super().__init__(**kwargs)

        self.gps_marker = None

        self.ap_markers = []
        self.bt_markers = []

        self._gps_event = None

        self._aps_event = None
        self._bt_event = None

        self._lp_touch = None
        self._long_press_trigger = Clock.create_trigger(
            self._trigger_long_press,
            0.5,
            interval=False,
        )

        self.track_points = []

        self.track_layer = None

        self.ruler_points = []

        self.area_points = []

        self.breadcrumb = []

        self._compass_heading = 0.0

        self.kml_layers = []

        self.geofences = []
        self._cluster_capacity = 8
        self._last_gps = None
        self._last_time = 0.0
        self._gps_interval = 0.0
        try:
            self._gps_client = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        except Exception:  # pragma: no cover - gpsd unavailable
            self._gps_client = None
        self._http = requests.Session()




    def on_enter(self):  # pylint: disable=arguments-differ

        """Start GPS and AP polling when entering the screen."""

        app = App.get_running_app()

        if app.map_use_offline:

            try:

                self.ids.mapview.map_source = MBTilesMapSource(app.offline_tile_path)

            except Exception as e:

                report_error(f"Offline tiles error: {e}")

        self._gps_event = "map_gps"

        self._aps_event = "map_aps"

        app.scheduler.schedule(

            self._gps_event, lambda dt: self.center_on_gps(), app.map_poll_gps

        )

        app.scheduler.schedule(

            self._aps_event, lambda dt: self.plot_aps(), app.map_poll_aps

        )
        self._bt_event = "map_bt"
        app.scheduler.schedule(
            self._bt_event, lambda dt: self.plot_bt_devices(), app.map_poll_bt
        )
        # React to zoom level changes by updating clusters
        self.ids.mapview.bind(zoom=self.update_clusters_on_zoom)

        if getattr(app, "app_state", None) and app.app_state.first_run:
            Clock.schedule_once(lambda _dt: self.start_first_run_tour(), 0.5)



    def on_leave(self):  # pylint: disable=arguments-differ

        """Unschedule polling tasks when leaving the screen."""

        app = App.get_running_app()

        if self._gps_event:
            app.scheduler.cancel(self._gps_event)
            self._gps_event = None
        if self._aps_event:
            app.scheduler.cancel(self._aps_event)
            self._aps_event = None
        if self._bt_event:
            app.scheduler.cancel(self._bt_event)
            self._bt_event = None

# ------------------------------------------------------------------

    # Touch handlers
    def _map_touch_down(self, _mapview, touch):

        """Schedule long press detection."""

        if _mapview.collide_point(*touch.pos):
            self._lp_touch = touch
            self._long_press_trigger()



    def _map_touch_move(self, _mapview, touch):

        """Cancel long press if the touch moves too far."""

        if self._lp_touch and (abs(touch.dx) > dp(10) or abs(touch.dy) > dp(10)):
            self._long_press_trigger.cancel()
            self._lp_touch = None



    def _map_touch_up(self, _mapview, touch):

        """Cancel pending long press on touch release."""

        if self._lp_touch:
            self._long_press_trigger.cancel()
            self._lp_touch = None



    def _on_long_press(self, touch):

        """Handle a confirmed long press gesture."""

        mv = self.ids.mapview

        lat, lon = mv.get_latlon_at(touch.x, touch.y)

        self._show_context_menu(lat, lon, touch.pos)


    def _trigger_long_press(self, _dt):
        if self._lp_touch is not None:
            self._on_long_press(self._lp_touch)
            self._lp_touch = None



    def _show_context_menu(self, lat, lon, _pos):

        """Open a context menu for map actions at the given position."""

        items = [

            {

                "text": "Center here",

                "viewclass": "OneLineListItem",

                "on_release": lambda *a: (

                    self.ids.mapview.center_on(lat, lon),

                    self.context_menu.dismiss(),

                ),

            },

            {

                "text": "Save this location",

                "viewclass": "OneLineListItem",

                "on_release": lambda *a: (

                    self.save_waypoint(lat, lon),

                    self.context_menu.dismiss(),

                ),

            },

            {

                "text": "Load GPX Track",

                "viewclass": "OneLineListItem",

                "on_release": lambda *a: (

                    self.load_gpx_prompt(),

                    self.context_menu.dismiss(),

                ),

            },

            {

                "text": "Load KML/KMZ",

                "viewclass": "OneLineListItem",

                "on_release": lambda *a: (

                    self.load_kml_prompt(),

                    self.context_menu.dismiss(),

                ),

            },

            {

                "text": "Measure distance",

                "viewclass": "OneLineListItem",

                "on_release": lambda *a: self.start_ruler_mode(),

            },

        ]

        self.context_menu = MDDropdownMenu(

            caller=self.ids.mapview, items=items, width_mult=3, max_height=dp(150)

        )

        self.context_menu.open()



    def save_waypoint(self, lat, lon):

        """Persist a waypoint to the user's config directory."""

        path = os.path.join(

            os.path.expanduser("~"), ".config", "piwardrive", "waypoints.json"

        )

        os.makedirs(os.path.dirname(path), exist_ok=True)

        data = []

        try:

            with open(path, "r", encoding="utf-8") as fh:

                data = json.load(fh)

        except Exception:

            data = []

        data.append({"lat": lat, "lon": lon, "ts": time.time()})

        with open(path, "w", encoding="utf-8") as fh:

            json.dump(data, fh, indent=2)

        Snackbar(text="Waypoint saved").open()



    def load_gpx_prompt(self):

        """Prompt the user for a GPX file path and load it."""

        self.gpx_field = MDTextField(

            hint_text="GPX file path",

            size_hint_x=0.8,

            pos_hint={"center_x": 0.5, "center_y": 0.6},

        )

        self.gpx_dialog = MDDialog(

            title="Load GPX", type="custom", content_cls=self.gpx_field, buttons=[]

        )

        self.gpx_dialog.open()

        self.gpx_field.bind(on_text_validate=lambda x: self._load_gpx(x.text))



    def _load_gpx(self, path):

        self.gpx_dialog.dismiss()

        try:

            points = []

            import xml.etree.ElementTree as ET



            tree = ET.parse(path)

            for trkpt in tree.findall(".//{*}trkpt"):

                lat = float(trkpt.get("lat"))

                lon = float(trkpt.get("lon"))

                points.append((lat, lon))

            if points:

                mv = self.ids.mapview

                layer = LineMapLayer(points=points)

                mv.add_layer(layer)

                Snackbar(text="Track loaded").open()

        except Exception as e:

            report_error(f"GPX load error: {e}")



    def load_kml_prompt(self):

        """Prompt the user for a KML or KMZ file path and load it."""

        self.kml_field = MDTextField(

            hint_text="KML/KMZ file path",

            size_hint_x=0.8,

            pos_hint={"center_x": 0.5, "center_y": 0.6},

        )

        self.kml_dialog = MDDialog(

            title="Load KML/KMZ", type="custom", content_cls=self.kml_field, buttons=[]

        )

        self.kml_dialog.open()

        self.kml_field.bind(on_text_validate=lambda x: self._load_kml(x.text))



    def _load_kml(self, path):

        self.kml_dialog.dismiss()

        try:

            features = load_kml(path)

            mv = self.ids.mapview

            for feat in features:

                if feat["type"] == "Point":

                    m = MapMarker(

                        lat=feat["coordinates"][0],

                        lon=feat["coordinates"][1],

                        source="widgets/marker-ap.png",

                        anchor_x="center",

                        anchor_y="center",

                    )

                    mv.add_widget(m)

                    self.kml_layers.append(m)

                elif feat["type"] == "LineString":

                    layer = LineMapLayer(points=feat["coordinates"])

                    mv.add_layer(layer)

                    self.kml_layers.append(layer)

                elif feat["type"] == "Polygon":

                    layer = LineMapLayer(

                        points=feat["coordinates"] + [feat["coordinates"][0]]

                    )

                    mv.add_layer(layer)

                    self.kml_layers.append(layer)

                    # polygon also acts as geofence

                    self.add_geofence(feat["name"] or "geofence", feat["coordinates"])

            Snackbar(text="Geodata loaded").open()

        except Exception as e:

            report_error(f"KML load error: {e}")



    # GPS centering



    def center_on_gps(self):

        """Center the map on the current GPS location."""

        app = App.get_running_app()

        if not app.map_show_gps:

            return

        threading.Thread(target=self._fetch_and_center, daemon=True).start()



    def _fetch_and_center(self):

        """Fetch GPS coordinates in a thread and center the map."""
        if self._gps_client is None:
            return
        try:
            report = self._gps_client.next()
            lat = getattr(report, "lat", None)
            lon = getattr(report, "lon", None)
            if lat is not None and lon is not None:
                self._update_map(lat, lon)
                self._adjust_gps_interval(lat, lon)
        except StopIteration:
            report_error("GPS lock timed out")
        except Exception as e:

            pos = gps_client.get_position()
            if pos:
                lat, lon = pos
                self._update_map(lat, lon)
                self._adjust_gps_interval(lat, lon)
            else:
                report_error("GPS lock timed out")
        except Exception as e:  # pragma: no cover - unexpected
            report_error(f"GPS error: {e}")



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

                lat=lat,

                lon=lon,

                source="widgets/center-icon.png",

                anchor_x="center",

                anchor_y="center",

            )

            mv.add_widget(self.gps_marker)

        self._check_geofences(lat, lon)


    def _adjust_gps_interval(self, lat: float, lon: float) -> None:
        """Dynamically adjust GPS polling based on movement speed."""
        app = App.get_running_app()
        now = time.time()
        if self._last_gps is not None and self._last_time:
            dist = haversine_distance(self._last_gps, (lat, lon))
            dt = now - self._last_time
            speed = dist / dt if dt > 0 else 0.0
        else:
            speed = 0.0
        self._last_gps = (lat, lon)
        self._last_time = now
        interval = app.map_poll_gps if speed > 1 else app.map_poll_gps_max
        if interval != self._gps_interval:
            self._gps_interval = interval
            Clock.schedule_once(
                lambda _dt, iv=interval: app.scheduler.schedule(
                    self._gps_event, lambda dt: self.center_on_gps(), iv
                )
            )


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
        clustering = app.map_cluster_aps



        try:
            resp = self._http.get(
                "http://127.0.0.1:2501/devices/all.json", timeout=5
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            self._show_error(f"AP overlay request error: {e}")
            data = {"devices": []}
        except json.JSONDecodeError as e:
            self._show_error(f"AP overlay JSON decode error: {e}")
            data = {"devices": []}
        except Exception as e:  # pragma: no cover - unexpected
            self._show_error(f"AP overlay error: {e}")
            data = {"devices": []}

        # merge in SIGINT scan exports
        try:
            from sigint_integration import load_sigint_data

            for rec in load_sigint_data("wifi"):
                if "lat" in rec and "lon" in rec:
                    data.setdefault("devices", []).append(
                        {
                            "bssid": rec.get("bssid"),
                            "ssid": rec.get("ssid"),
                            "encryption": rec.get("encryption"),
                            "gps-info": [rec["lat"], rec["lon"], 0],
                        }
                    )
        except Exception:
            pass

        for d in data.get("devices", []):
            gps = d.get("gps-info")
            if (not gps or len(gps) < 2) and d.get("observations"):
                loc = export.estimate_location_from_rssi(d.get("observations", []))
                if loc is not None:
                    gps = [loc[0], loc[1], 0]

            if gps and len(gps) >= 2:
                m = MapMarkerPopup(
                    lat=gps[0],
                    lon=gps[1],
                    source="widgets/marker-ap.png",
                    anchor_x="center",
                    anchor_y="center",
                )
                m.add_widget(
                    Label(
                        text=d.get("bssid", "AP"),
                        size_hint=(None, None),
                        size=(dp(80), dp(20)),
                    )
                )
                m.ap_data = {
                    "bssid": d.get("bssid"),
                    "ssid": d.get("ssid"),
                    "encryption": d.get("encryption"),
                }
                mv.add_widget(m)
                self.ap_markers.append(m)

        if clustering:
            # group nearby markers based on current zoom level
            self.update_clusters_on_zoom(mv, mv.zoom)


    def plot_bt_devices(self):
        """Render Bluetooth device markers on the map."""
        app = App.get_running_app()
        if not app.map_show_bt:
            return
        mv = self.ids.mapview
        for m in self.bt_markers:
            mv.remove_widget(m)
        self.bt_markers.clear()
        devices = utils.scan_bt_devices()
        try:
            from sigint_integration import load_sigint_data

            devices.extend(load_sigint_data("bluetooth"))
        except Exception:
            pass
        for d in devices:
            lat = d.get("lat")
            lon = d.get("lon")
            if lat is None or lon is None:
                continue
            m = MapMarkerPopup(
                lat=lat,
                lon=lon,
                source="widgets/marker-ap.png",
                anchor_x="center",
                anchor_y="center",
            )
            m.add_widget(
                Label(
                    text=d.get("name", d.get("address", "BT")),
                    size_hint=(None, None),
                    size=(dp(80), dp(20)),
                )
            )
            mv.add_widget(m)
            self.bt_markers.append(m)





    # Layer menu

    def show_layer_menu(self, widget):

        """Display the layer toggle dropdown menu."""

        items = [

            {

                "text": "GPS Marker",

                "viewclass": "OneLineListItem",

                "on_release": lambda *a, k="map_show_gps": self._toggle(k),

            },

            {

                "text": "AP Markers",

                "viewclass": "OneLineListItem",

                "on_release": lambda *a, k="map_show_aps": self._toggle(k),

            },

            {

                "text": "BT Markers",

                "viewclass": "OneLineListItem",

                "on_release": lambda *a, k="map_show_bt": self._toggle(k),

            },

            {

                "text": "Cluster APs",

                "viewclass": "OneLineListItem",

                "on_release": lambda *a, k="map_cluster_aps": self._toggle(k),

            },

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

    def start_first_run_tour(self):
        self._tour_hints = [
            "Tap ⛶ to center on GPS",
            "Tap +/– to zoom in or out",
            "Long-press anywhere for more options",
        ]
        self._tour_index = 0
        self._show_next_tour_hint()

    def _show_next_tour_hint(self, _dt=None):
        if self._tour_index >= len(self._tour_hints):
            app = App.get_running_app()
            app.app_state.first_run = False
            try:
                asyncio.run(save_app_state(app.app_state))
            except Exception:  # pragma: no cover - best effort
                pass
            return
        Snackbar(text=self._tour_hints[self._tour_index], duration=3).open()
        self._tour_index += 1
        Clock.schedule_once(self._show_next_tour_hint, 3.5)



    # Helpers



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

    async def _download_tile_async(self, session, url, local):
        from .map_utils import tile_cache
        await tile_cache.download_tile_async(session, url, local)



    # ------------------------------------------------------------------

    # Offline Map Tile Management

    # tile management helpers moved to :mod:`screens.map_utils.tile_cache`

    async def _download_tile_async(
        self, session: aiohttp.ClientSession, url: str, local: str
    ) -> None:
        """Fetch a single map tile."""
        from .map_utils import tile_cache

        await tile_cache.download_tile_async(session, url, local)


    def prefetch_tiles(
        self,
        bounds,
        zoom: int = 16,
        folder: str = "/mnt/ssd/tiles",
        *,
        concurrency: int | None = None,
        progress_cb: Callable[[int, int], None] | None = None,
    ) -> None:
        """Download PNG tiles covering ``bounds`` to ``folder``."""

        try:
            from .map_utils import tile_cache

            tile_cache.prefetch_tiles(
                bounds,
                zoom=zoom,
                folder=folder,
                concurrency=concurrency,
                progress_cb=progress_cb,
            )
        except Exception as e:  # pragma: no cover - network errors
            report_error(f"Prefetch error: {e}")


    async def _download_tile_async(self, session, url: str, local: str) -> None:
        """Fetch a single tile from ``url`` into ``local`` asynchronously."""
        async with session.get(url) as resp:
            resp.raise_for_status()
            data = await resp.read()
        os.makedirs(os.path.dirname(local), exist_ok=True)
        with open(local, "wb") as fh:
            fh.write(data)

    def prefetch_tiles(self, bounds, zoom: int = 16, folder: str = "/mnt/ssd/tiles", *, concurrency: int | None = None, progress_cb: Callable[[int, int], None] | None = None) -> None:
        try:
            from .map_utils import tile_cache
            tile_cache.prefetch_tiles(bounds, zoom=zoom, folder=folder, concurrency=concurrency, progress_cb=progress_cb)
        except Exception as e:  # pragma: no cover - network errors
            report_error(f"Prefetch error: {e}")

    def prefetch_visible_region(self):
        """Download tiles for the current view if offline mode is active."""
        app = App.get_running_app()
        if not getattr(app, "map_use_offline", False):
            Snackbar(text="Enable offline tiles first").open()
            return
        mv = self.ids.get("mapview")
        if mv is None:
            return

        bbox = mv.get_bbox()
        folder = os.path.dirname(getattr(app, "offline_tile_path", "")) or "/mnt/ssd/tiles"

        progress_bar = MDProgressBar(value=0)
        progress_label = MDLabel(text="0/0", halign="center")
        content = MDBoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None, height=dp(56))
        content.add_widget(progress_label)
        content.add_widget(progress_bar)
        dialog = MDDialog(title="Prefetching tiles", type="custom", content_cls=content)
        dialog.open()

        def progress(done: int, total: int) -> None:
            def _update(_dt):
                target = done / total * 100 if total else 100
                Animation.cancel_all(progress_bar)
                Animation(value=target, duration=0.2).start(progress_bar)
                progress_label.text = f"{done}/{total}"
                if done >= total:
                    dialog.dismiss()
                    Snackbar(text="Prefetch complete").open()
            Clock.schedule_once(_update)

        def _worker() -> None:
            self.prefetch_tiles(tuple(bbox), zoom=mv.zoom, folder=folder, progress_cb=progress)

        threading.Thread(target=_worker, daemon=True).start()



    def purge_old_tiles(self, max_age_days=30, folder="/mnt/ssd/tiles"):

        """Delete cached tiles older than ``max_age_days`` days."""

        cutoff = time.time() - max_age_days * 86400

        try:
            if not os.path.isdir(folder):
                return

            for root, _, files in os.walk(folder):
                for f in files:
                    path = os.path.join(root, f)
                    if os.path.getmtime(path) < cutoff:
                        os.remove(path)
        except Exception as e:  # pragma: no cover - filesystem errors
            report_error(f"Tile purge error: {e}")



    def enforce_cache_limit(self, folder="/mnt/ssd/tiles", limit_mb=512):

        """Ensure tile cache does not exceed ``limit_mb`` megabytes."""

        try:
            if not os.path.isdir(folder):
                return

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
        except Exception as e:  # pragma: no cover - filesystem errors
            report_error(f"Cache limit error: {e}")



    # ------------------------------------------------------------------

    # Thematic Layers & Filtering

    def filter_ap_markers(self, ssid=None, encryption=None, oui=None):

        """Filter AP markers based on SSID, encryption type, or MAC OUI."""

        for m in self.ap_markers:

            data = getattr(m, "ap_data", {})

            visible = True

            if ssid and ssid not in (data.get("ssid") or ""):

                visible = False

            if encryption and encryption != data.get("encryption"):

                visible = False

            if oui and not (data.get("bssid") or "").startswith(oui):

                visible = False

            m.opacity = 1 if visible else 0



    def apply_icon_set(self, icon_map):

        """Update AP marker icons according to ``icon_map`` keyed by encryption."""

        for m in self.ap_markers:

            data = getattr(m, "ap_data", {})

            enc = data.get("encryption")

            if enc in icon_map:

                m.source = icon_map[enc]



    # ------------------------------------------------------------------

    # Map Orientation & Sensors

    def update_compass(self, heading):

        """Rotate map view to match the given compass ``heading``."""

        self._compass_heading = heading

        self.ids.mapview.rotation = -heading






    def register_sensor(self, name, handler):

        """Store additional sensor handler for future use."""

        setattr(self, f"sensor_{name}", handler)



    # ------------------------------------------------------------------

    # Geofence Handling

    def add_geofence(self, name, polygon, on_enter=None, on_exit=None):

        """Register a geofence polygon with optional enter/exit callbacks."""

        self.geofences.append(

            {

                "name": name,

                "polygon": polygon,

                "inside": False,

                "on_enter": on_enter,

                "on_exit": on_exit,

            }

        )



    def _check_geofences(self, lat, lon):

        """Check all geofences for crossings."""

        for gf in self.geofences:

            inside = point_in_polygon((lat, lon), gf["polygon"])

            if inside and not gf["inside"]:

                gf["inside"] = True

                if gf["on_enter"]:

                    gf["on_enter"](gf["name"])

            elif not inside and gf["inside"]:

                gf["inside"] = False

                if gf["on_exit"]:

                    gf["on_exit"](gf["name"])



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

        data = [getattr(m, "ap_data", {}) for m in self.ap_markers]

        try:
            if data:
                fieldnames = list(data[0].keys())
                with open(path, "w", newline="", encoding="utf-8") as fh:
                    writer = csv.DictWriter(fh, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
            else:
                open(path, "w", encoding="utf-8").close()

            if not data:
                open(path, "w", encoding="utf-8").close()
            else:
                fieldnames = sorted({k for d in data for k in d.keys()})
                with open(path, "w", encoding="utf-8", newline="") as fh:
                    writer = csv.DictWriter(fh, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)


            Snackbar(text=f"Exported {path}").open()

        except Exception as e:

            report_error(f"Export error: {e}")



    def create_pdf_snapshot(self, path):

        """Generate a PDF of the current map view."""

        png_path = f"{path}.png"

        self.ids.mapview.export_to_png(png_path)

        try:

            import img2pdf



            with open(path, "wb") as fh:

                fh.write(img2pdf.convert(png_path))

            os.remove(png_path)

            Snackbar(text=f"Saved {path}").open()

        except Exception as e:

            report_error(f"PDF export error: {e}")

    def export_full_kml(self, path, *, compute_position: bool = False):
        """Export GPS track and markers to ``path`` as KML or KMZ."""
        ap_records = [
            {**getattr(m, "ap_data", {}), "lat": m.lat, "lon": m.lon}
            for m in self.ap_markers
        ]
        bt_records = [
            {
                "name": getattr(m, "bt_name", None),
                "address": getattr(m, "bt_address", None),
                "lat": m.lat,
                "lon": m.lon,
            }
            for m in self.bt_markers
        ]
        try:
            export.export_map_kml(
                self.track_points,
                ap_records,
                bt_records,
                path,
                compute_position=compute_position,
            )
            Snackbar(text=f"Exported {path}").open()
        except Exception as e:
            report_error(f"Export error: {e}")



    # ------------------------------------------------------------------

    # Clustering Behaviors

    def update_clusters_on_zoom(self, _mapview, zoom):
        """Cluster markers dynamically when the map is zoomed."""

        if not self.ap_markers:
            return

        # Calculate grid cell size so that fewer clusters are formed when
        # zoomed out and more clusters when zoomed in. ``_cluster_capacity``
        # controls how many markers may occupy a cell before collapsing.
        cell_size = 360 / (2 ** zoom * self._cluster_capacity)

        # Group markers by their grid cell
        clusters: dict[tuple[int, int], list] = {}
        for marker in self.ap_markers:
            key = (int(marker.lat / cell_size), int(marker.lon / cell_size))
            clusters.setdefault(key, []).append(marker)

        # Replace each group of markers by their averaged position
        for group in clusters.values():
            if len(group) <= 1:
                continue
            lat = sum(m.lat for m in group) / len(group)
            lon = sum(m.lon for m in group) / len(group)
            for marker in group:
                marker.lat = lat
                marker.lon = lon

        # Spread markers that still overlap exactly
        self.spiderfy_markers()



    def spiderfy_markers(self):
        """Spread markers that have identical positions."""

        groups: dict[tuple[float, float], list] = {}
        for m in self.ap_markers:
            key = (round(m.lat, 6), round(m.lon, 6))
            groups.setdefault(key, []).append(m)

        for markers in groups.values():
            if len(markers) <= 1:
                continue
            base_lat = markers[0].lat
            base_lon = markers[0].lon
            radius = 0.0001
            step = 2 * math.pi / len(markers)
            for i, mk in enumerate(markers):
                angle = i * step
                mk.lat = base_lat + radius * math.cos(angle)
                mk.lon = base_lon + radius * math.sin(angle)



    def adjust_quadtree(self, capacity):
        """Adjust clustering cell capacity and refresh clusters."""

        try:
            val = int(capacity)
        except (TypeError, ValueError):
            return
        self._cluster_capacity = max(1, val)
        mv = self.ids.get("mapview")
        if mv:
            self.update_clusters_on_zoom(mv, mv.zoom)



    # ------------------------------------------------------------------

    # Custom Marker Styles

    def update_marker_icons(self, icon_map):

        """Apply icons based on encryption type using ``icon_map`` mapping."""

        self.apply_icon_set(icon_map)



    def set_directional_marker(self, marker, bearing):

        """Rotate ``marker`` to indicate relative ``bearing``."""

        marker.rotation = bearing
