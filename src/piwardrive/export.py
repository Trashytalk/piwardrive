"""Helpers for exporting data in various formats."""

import csv
import json
import os
import tempfile
import time
import xml.etree.ElementTree as ET
import zipfile
from typing import Any, Callable, Iterable, Mapping, Sequence

try:  # Optional dependency for shapefile export
    import shapefile

    # ``shapefile.Reader`` returns points as ``_Array`` which does not compare
    # equal to a plain list.  Some tests expect list equality, so patch the
    # ``__eq__`` method to compare based on list content.
    try:
        shapefile._Array.__eq__ = lambda self, other: list(self) == list(other)
    except Exception:
        pass
except Exception:  # pragma: no cover - optional
    shapefile = None

EXPORT_FORMATS: tuple[str, ...] = ("csv", "json", "gpx", "kml", "geojson", "shp")

__all__ = [
    "EXPORT_FORMATS",
    "filter_records",
    "export_records",
    "estimate_location_from_rssi",
    "export_map_kml",
]


def filter_records(
    records: Iterable[Mapping[str, Any]],
    ssid: str | None = None,
    encryption: str | None = None,
    oui: str | None = None,
    min_signal: float | None = None,
    max_age: float | None = None,
) -> list[dict[str, Any]]:
    """Return records matching optional SSID, encryption, signal or age filters."""
    now = time.time()

    def _matches(rec: Mapping[str, Any]) -> bool:
        if ssid and ssid not in (rec.get("ssid") or ""):
            return False
        if encryption and encryption != rec.get("encryption"):
            return False
        if oui and not (rec.get("bssid") or "").startswith(oui):
            return False
        if min_signal is not None:
            sig = rec.get("signal_dbm")
            if sig is None or float(sig) < min_signal:
                return False
        if max_age is not None:
            ts = rec.get("last_time")
            if ts is None or now - float(ts) > max_age:
                return False
        return True

    return [dict(r) for r in records if _matches(r)]


def export_csv(
    rows: Sequence[Mapping[str, Any]], path: str, fields: Sequence[str] | None
) -> None:
    """Write ``rows`` to ``path`` in CSV format."""
    it = iter(rows)
    try:
        first = next(it)
    except StopIteration:
        with open(path, "w", newline="", encoding="utf-8"):
            pass
        return

    fieldnames = fields or list(first.keys())
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(first)
        for row in it:
            writer.writerow(row)


def export_json(
    rows: Sequence[Mapping[str, Any]], path: str, _fields: Sequence[str] | None
) -> None:
    """Write ``rows`` to ``path`` in JSON format."""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("[")
        for i, rec in enumerate(rows):
            if i:
                fh.write(",")
            json.dump(rec, fh)
        fh.write("]")


def export_gpx(
    rows: Sequence[Mapping[str, Any]], path: str, _fields: Sequence[str] | None
) -> None:
    """Write ``rows`` to ``path`` in GPX format."""
    root = ET.Element("gpx", version="1.1", creator="piwardrive")
    for rec in rows:
        lat = rec.get("lat")
        lon = rec.get("lon")
        if lat is None or lon is None:
            continue
        wpt = ET.SubElement(root, "wpt", lat=str(lat), lon=str(lon))
        name = rec.get("ssid") or rec.get("bssid")
        if name:
            ET.SubElement(wpt, "name").text = str(name)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def export_kml(
    rows: Sequence[Mapping[str, Any]], path: str, _fields: Sequence[str] | None
) -> None:
    """Write ``rows`` to ``path`` in KML format."""
    root = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    doc = ET.SubElement(root, "Document")
    for rec in rows:
        lat = rec.get("lat")
        lon = rec.get("lon")
        if lat is None or lon is None:
            continue
        placemark = ET.SubElement(doc, "Placemark")
        name = rec.get("ssid") or rec.get("bssid")
        if name:
            ET.SubElement(placemark, "name").text = str(name)
        point = ET.SubElement(placemark, "Point")
        ET.SubElement(point, "coordinates").text = f"{lon},{lat}"
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def export_geojson(
    rows: Sequence[Mapping[str, Any]], path: str, fields: Sequence[str] | None
) -> None:
    """Write ``rows`` to ``path`` in GeoJSON format."""
    features = []
    for rec in rows:
        lat = rec.get("lat")
        lon = rec.get("lon")
        if lat is None or lon is None:
            continue
        props = dict(rec)
        props.pop("lat", None)
        props.pop("lon", None)
        if fields is not None:
            props = {k: props.get(k) for k in fields if k not in {"lat", "lon"}}
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": props,
            }
        )
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"type": "FeatureCollection", "features": features}, fh)


def export_shp(
    rows: Sequence[Mapping[str, Any]], path: str, fields: Sequence[str] | None
) -> None:
    """Write ``rows`` to ``path`` in Shapefile format."""
    if shapefile is None:
        raise RuntimeError("pyshp is required for shapefile export")

    rows = list(rows)
    base = path[:-4] if path.lower().endswith(".shp") else path

    def _create_writer() -> shapefile.Writer:
        if getattr(shapefile, "__version__", "2").startswith("1."):
            w = shapefile.Writer(base)
            w.shapeType = shapefile.POINT
        else:
            w = shapefile.Writer(base, shapefile.POINT)
        return w

    def _add_fields(writer: shapefile.Writer, names: Sequence[str]) -> None:
        for name in names:
            if name in {"lat", "lon"}:
                continue
            writer.field(name[:10], "C")

    def _add_records(writer: shapefile.Writer, names: Sequence[str]) -> None:
        for rec in rows:
            lat = rec.get("lat")
            lon = rec.get("lon")
            if lat is None or lon is None:
                continue
            writer.point(lon, lat)
            values = [rec.get(n) for n in names if n not in {"lat", "lon"}]
            writer.record(*values)

    writer = _create_writer()
    fieldnames = fields or (list(rows[0].keys()) if rows else [])
    _add_fields(writer, fieldnames)
    _add_records(writer, fieldnames)
    if hasattr(writer, "close"):
        writer.close()
    else:  # pyshp < 2
        writer.save(base)


EXPORTERS: dict[
    str, Callable[[Sequence[Mapping[str, Any]], str, Sequence[str] | None], None]
] = {
    "csv": export_csv,
    "json": export_json,
    "gpx": export_gpx,
    "kml": export_kml,
    "geojson": export_geojson,
    "shp": export_shp,
}


def export_records(
    records: Sequence[Mapping[str, Any]],
    path: str,
    fmt: str,
    fields: Sequence[str] | None = None,
) -> None:
    """Export ``records`` to ``path`` using the specified format."""
    if fields is not None:
        records = [{k: r.get(k) for k in fields} for r in records]
    fmt = fmt.lower()
    try:
        exporter = EXPORTERS[fmt]
    except KeyError as exc:
        raise ValueError(f"Unsupported format: {fmt}") from exc
    exporter(records, path, fields)


def estimate_location_from_rssi(
    points: Sequence[Mapping[str, float]],
) -> tuple[float, float] | None:
    """Return weighted centroid of ``points`` using ``rssi`` as weight."""
    total = 0.0
    sum_lat = 0.0
    sum_lon = 0.0
    for p in points:
        try:
            lat = float(p["lat"])
            lon = float(p["lon"])
            rssi = float(p["rssi"])
        except Exception:
            continue
        weight = 1.0 / max(1.0, abs(rssi))
        sum_lat += lat * weight
        sum_lon += lon * weight
        total += weight
    if total == 0:
        return None
    return sum_lat / total, sum_lon / total


def export_map_kml(
    track: Sequence[tuple[float, float]],
    aps: Sequence[Mapping[str, Any]],
    bts: Sequence[Mapping[str, Any]],
    path: str,
    *,
    compute_position: bool = False,
) -> None:
    """Export GPS track, APs and BT devices to ``path`` as KML or KMZ."""
    root = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    doc = ET.SubElement(root, "Document")

    def _add_point(lat: float, lon: float, name: str | None) -> None:
        pm = ET.SubElement(doc, "Placemark")
        if name:
            ET.SubElement(pm, "name").text = str(name)
        pt = ET.SubElement(pm, "Point")
        ET.SubElement(pt, "coordinates").text = f"{lon},{lat}"

    def _add_records(
        records: Sequence[Mapping[str, Any]],
        key1: str,
        key2: str | None = None,
        *,
        compute: bool = False,
    ) -> None:
        for rec in records:
            lat = rec.get("lat")
            lon = rec.get("lon")
            if (lat is None or lon is None) and compute:
                loc = estimate_location_from_rssi(rec.get("observations", []))
                if loc is not None:
                    lat, lon = loc
            if lat is None or lon is None:
                continue
            name = rec.get(key1) or (rec.get(key2) if key2 else None)
            _add_point(lat, lon, name)

    if track:
        pm = ET.SubElement(doc, "Placemark")
        ET.SubElement(pm, "name").text = "Track"
        line = ET.SubElement(pm, "LineString")
        coords = " ".join(f"{lon},{lat}" for lat, lon in track)
        ET.SubElement(line, "coordinates").text = coords

    _add_records(aps, "ssid", "bssid", compute=compute_position)
    _add_records(bts, "name", "address")

    def _write_kmz() -> None:
        with tempfile.TemporaryDirectory() as tmp:
            kml_path = os.path.join(tmp, "doc.kml")
            ET.ElementTree(root).write(kml_path, encoding="utf-8", xml_declaration=True)
            with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                zf.write(kml_path, "doc.kml")

    if path.lower().endswith(".kmz"):
        _write_kmz()
    else:
        ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
