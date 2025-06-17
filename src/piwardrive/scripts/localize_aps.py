"""CLI wrapper for advanced AP localization."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from advanced_localization import load_config, load_kismet_data, localize_aps

try:
    import folium
except Exception:  # pragma: no cover - optional dependency
    folium = None


def _save_map(coords: dict[str, tuple[float, float]], output: Path, zoom: int) -> None:
    if folium is None or not coords:
        return
    lats = [c[0] for c in coords.values()]
    lons = [c[1] for c in coords.values()]
    m = folium.Map(
        location=[sum(lats) / len(lats), sum(lons) / len(lons)],
        zoom_start=zoom,
    )
    for mac, (lat, lon) in coords.items():
        folium.Marker([lat, lon], popup=mac).add_to(m)
    m.save(str(output))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Estimate AP locations from a Kismet log"
    )
    parser.add_argument("database", help="Path to .kismet SQLite log")
    parser.add_argument(
        "--config", default="localization_config.json", help="Config JSON path"
    )
    parser.add_argument(
        "--output", default="ap_locations.html", help="Output HTML map"
    )
    args = parser.parse_args(argv)

    cfg = load_config(args.config)
    data = load_kismet_data(args.database)
    coords = localize_aps(data, cfg)

    if folium is not None:
        _save_map(coords, Path(args.output), cfg.map_zoom_start)
    else:
        print(json.dumps(coords, indent=2))


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
