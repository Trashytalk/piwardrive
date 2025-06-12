from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapView, MapMarker, MapMarkerPopup
from kivy.clock import Clock, mainthread
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.app import App
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar

import threading, subprocess, json, requests, time


class MapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gps_marker  = None
        self.ap_markers  = []
        self._gps_event  = None
        self._aps_event  = None
        self._lp_event   = None
        self._touch_time = None

    def on_enter(self):
        app = App.get_running_app()
        self._gps_event = Clock.schedule_interval(
            lambda dt: self.center_on_gps(), app.map_poll_gps
        )
        self._aps_event = Clock.schedule_interval(
            lambda dt: self.plot_aps(), app.map_poll_aps
        )

    def on_leave(self):
        if self._gps_event:
            Clock.unschedule(self._gps_event); self._gps_event = None
        if self._aps_event:
            Clock.unschedule(self._aps_event); self._aps_event = None
        if self._lp_event:
            Clock.unschedule(self._lp_event); self._lp_event = None

    # Long‐press detection scheduled on MapView
    def _map_touch_down(self, mapview, touch):
        if mapview.collide_point(*touch.pos):
            self._lp_event = Clock.schedule_once(
                lambda dt: self._on_long_press(touch), 0.5
            )

    def _map_touch_move(self, mapview, touch):
        if self._lp_event and abs(touch.dx) > dp(10) or abs(touch.dy) > dp(10):
            Clock.unschedule(self._lp_event)
            self._lp_event = None

    def _map_touch_up(self, mapview, touch):
        if self._lp_event:
            Clock.unschedule(self._lp_event)
            self._lp_event = None

    def _on_long_press(self, touch):
        mv = self.ids.mapview
        lat, lon = mv.get_latlon_at(touch.x, touch.y)
        self._show_context_menu(lat, lon, touch.pos)

    def _show_context_menu(self, lat, lon, pos):
        items = [
            {"text": "Center here", "viewclass": "OneLineListItem",
             "on_release": lambda *a: (self.ids.mapview.center_on(lat, lon),
                                       self.context_menu.dismiss())},
            {"text": "Add waypoint", "viewclass": "OneLineListItem",
             "on_release": lambda *a: self._show_not_implemented("Add waypoint")},
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

    # GPS centering
    def center_on_gps(self):
        app = App.get_running_app()
        if not app.map_show_gps:
            return
        threading.Thread(target=self._fetch_and_center, daemon=True).start()

    def _fetch_and_center(self):
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
        mv = self.ids.mapview
        mv.center_on(lat, lon)
        mv.zoom = 16

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
        app = App.get_running_app()
        setattr(app, key, not getattr(app, key))
        self.layer_menu.dismiss()
        Snackbar(text=f"{key} = {getattr(app, key)}", duration=1.5).open()

    # Search / Jump to coords
    def open_search_dialog(self):
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
        fname = f"logs/map_{int(time.time())}.png"
        self.ids.mapview.export_to_png(fname)
        Snackbar(text=f"Saved {fname}").open()

    # Fullscreen
    def toggle_fullscreen(self):
        app = App.get_running_app()
        app.map_fullscreen = not app.map_fullscreen
        root = app.root
        root.ids.nav_bar.opacity          = 0 if app.map_fullscreen else 1
        root.ids.diagnostics_bar.opacity  = 0 if app.map_fullscreen else 1
        root.ids.nav_bar.disabled         = app.map_fullscreen
        root.ids.diagnostics_bar.disabled = app.map_fullscreen

    # Help overlay
    def show_help_overlay(self):
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
        Snackbar(text=msg, duration=3).open()

    def _show_not_implemented(self, feature_name):
        Snackbar(text=f"{feature_name} not yet implemented", duration=2).open()
