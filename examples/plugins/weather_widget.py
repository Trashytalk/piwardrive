"""Example dashboard plugin that fetches weather data."""

from __future__ import annotations

import requests

from piwardrive.simpleui import Card as MDCard
from piwardrive.simpleui import Label as MDLabel
from piwardrive.simpleui import dp
from widgets.base import DashboardWidget


class WeatherWidget(DashboardWidget):
    """Display the current London temperature using the Open-Meteo API."""

    update_interval = 600.0  # 10 minutes

    def __init__(self, **kwargs: object) -> None:
        """Create widget layout and fetch initial data."""
        super().__init__(**kwargs)
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(text="Fetching weather...", halign="center")
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self) -> None:
        """Retrieve the temperature from the API."""
        try:
            resp = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": 51.5072,
                    "longitude": -0.1276,
                    "current_weather": True,
                },
                timeout=10,
            )
            data = resp.json()
            temp = data["current_weather"]["temperature"]
            self.label.text = f"London {temp}\N{DEGREE SIGN}C"
        except Exception as exc:  # pragma: no cover - network call
            self.label.text = f"Weather error: {exc}"
