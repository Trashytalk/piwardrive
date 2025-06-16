"""Screen for drawing and saving geofence polygons."""

from __future__ import annotations

import json
import os
from typing import Any, List, Tuple

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy_garden.mapview import MapView, LineMapLayer
from kivymd.uix.button import MDFlatButton

from config import CONFIG_DIR


class GeofenceEditor(Screen):
    """Interactive editor to create polygonal geofences."""

    GEOFENCE_FILE = os.path.join(CONFIG_DIR, "geofences.json")

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.mapview = MapView()
        self.add_widget(self.mapview)

        controls = BoxLayout(size_hint_y=None, height=dp(48))
        save_btn = MDFlatButton(text="Save", on_release=lambda *_: self.save_polygons())
        finish_btn = MDFlatButton(text="Finish", on_release=lambda *_: self.finish_polygon())
        controls.add_widget(save_btn)
        controls.add_widget(finish_btn)
        self.add_widget(controls)

        self.current: List[Tuple[float, float]] = []
        self.polygons: List[dict[str, Any]] = []
        self._line: LineMapLayer | None = None

        self.mapview.bind(on_touch_down=self._on_touch)
        self.load_polygons()

    # ------------------------------------------------------------------
    def _on_touch(self, mapview: MapView, touch: Any) -> None:  # pragma: no cover - GUI
        if mapview.collide_point(*touch.pos):
            lat, lon = mapview.get_latlon_at(touch.x, touch.y)
            self.add_point(lat, lon)

    def add_point(self, lat: float, lon: float) -> None:
        """Add a vertex to the current polygon."""
        self.current.append((lat, lon))
        if self._line:
            mapview = self.mapview
            if self._line in mapview._layers:  # type: ignore[attr-defined]
                mapview.remove_layer(self._line)
        if len(self.current) > 1:
            self._line = LineMapLayer(points=self.current + [self.current[0]])
            self.mapview.add_layer(self._line)

    def finish_polygon(self, name: str | None = None) -> None:
        """Store the current polygon and reset drawing state."""
        if not self.current:
            return
        self.polygons.append({"name": name or "geofence", "points": self.current[:]})
        self.current.clear()
        if self._line:
            self.mapview.remove_layer(self._line)
            self._line = None
        self.save_polygons()

    # ------------------------------------------------------------------
    def load_polygons(self) -> None:
        """Load polygons from :data:`GEOFENCE_FILE`."""
        try:
            with open(self.GEOFENCE_FILE, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, list):
                self.polygons = data
                for poly in self.polygons:
                    pts = poly.get("points", [])
                    if len(pts) > 1:
                        layer = LineMapLayer(points=pts + [pts[0]])
                        self.mapview.add_layer(layer)
        except FileNotFoundError:
            self.polygons = []

    def save_polygons(self) -> None:
        """Persist polygons to :data:`GEOFENCE_FILE`."""
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(self.GEOFENCE_FILE, "w", encoding="utf-8") as fh:
            json.dump(self.polygons, fh, indent=2)

