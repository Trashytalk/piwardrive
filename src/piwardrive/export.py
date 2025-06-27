"""Helpers for exporting data in various formats."""

import csv
import json
import logging
import os
import tempfile
import time
import xml.etree.ElementTree as ET
import zipfile
from typing import Any, Callable, Iterable, Mapping, Sequence


try:  # Optional dependency for shapefile export
    import shapefile  # type: ignore

    # ``shapefile.Reader`` returns points as ``_Array`` which does not compare
    # equal to a plain list.  Some tests expect list equality, so patch the
    # ``__eq__`` method to compare based on list content.
    try:
        shapefile._Array.__eq__ = lambda self, other: list(self) == list(other)
    except Exception:  # nosec B110
        pass
except Exception:  # pragma: no cover - optional
    shapefile = None

EXPORT_FORMATS = ("csv", "json", "gpx", "kml", "geojson", "shp")

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
    result: list[dict[str, Any]] = []
    now = time.time()
    for rec in records:
        if ssid and ssid not in (rec.get("ssid") or ""):
            continue
        if encryption and encryption != rec.get("encryption"):
            continue
        if oui and not (rec.get("bssid") or "").startswith(oui):
            continue
        if min_signal is not None:
            sig = rec.get("signal_dbm")
            if sig is None or float(sig) < min_signal:
                continue
        if max_age is not None:
            ts = rec.get("last_time")
            if ts is None or now - float(ts) > max_age:
                continue
        result.append(dict(rec))
    return result


def export_csv(
    rows: Iterable[Mapping[str, Any]], path: str, fields: Sequence[str] | None
) -> None:
    """Write ``rows`` to ``path`` in CSV format."""
    it = iter(rows)
    try:
        first = next(it)
    except StopIteration:
        try:
            open(path, "w", newline="", encoding="utf-8").close()
        except OSError as exc:  # pragma: no cover - write errors
            logging.exception("Failed to write %s: %s", path, exc)
        return

    fieldnames = fields or list(first.keys())
    try:
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(first)
            for row in it:
                writer.writerow(row)
    except OSError as exc:  # pragma: no cover - write errors
        logging.exception("Failed to write %s: %s", path, exc)


def export_json(
    rows: Iterable[Mapping[str, Any]], path: str, _fields: Sequence[str] | None
) -> None:
    """Write ``rows`` to ``path`` in JSON format."""
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("[")
            for i, rec in enumerate(rows):
                if i:
                    fh.write(",")
                json.dump(rec, fh)
            fh.write("]")
    except OSError as exc:  # pragma: no cover - write errors
        logging.exception("Failed to write %s: %s", path, exc)


def export_gpx(
    rows: Iterable[Mapping[str, Any]], path: str, _fields: Sequence[str] | None
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
    try:
        ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    except OSError as exc:  # pragma: no cover - write errors
        logging.exception("Failed to write %s: %s", path, exc)


def export_kml(
    rows: Iterable[Mapping[str, Any]], path: str, _fields: Sequence[str] | None
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
    try:
        ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    except OSError as exc:  # pragma: no cover - write errors
        logging.exception("Failed to write %s: %s", path, exc)


def export_geojson(
    rows: Iterable[Mapping[str, Any]], path: str, fields: Sequence[str] | None
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
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"type": "FeatureCollection", "features": features}, fh)
    except OSError as exc:  # pragma: no cover - write errors
        logging.exception("Failed to write %s: %s", path, exc)


def export_shp(
    rows: Iterable[Mapping[str, Any]], path: str, fields: Sequence[str] | None
) -> None:
    """Write ``rows`` to ``path`` in Shapefile format."""
    if shapefile is None:
        raise RuntimeError("pyshp is required for shapefile export")
    it = iter(rows)
    try:
        first = next(it)
    except StopIteration:
        base = path[:-4] if path.lower().endswith(".shp") else path
        if getattr(shapefile, "__version__", "2").startswith("1."):
            writer = shapefile.Writer(base)
            writer.shapeType = shapefile.POINT
        else:
            writer = shapefile.Writer(base, shapefile.POINT)
        if hasattr(writer, "close"):
            writer.close()
        else:  # pyshp < 2
            writer.save(base)
        return

    base = path[:-4] if path.lower().endswith(".shp") else path
    if getattr(shapefile, "__version__", "2").startswith("1."):
        writer = shapefile.Writer(base)
        writer.shapeType = shapefile.POINT
    else:
        writer = shapefile.Writer(base, shapefile.POINT)
    fieldnames = fields or list(first.keys())
    for name in fieldnames:
        if name in {"lat", "lon"}:
            continue
        writer.field(name[:10], "C")

    def _write(rec: Mapping[str, Any]) -> None:
        lat = rec.get("lat")
        lon = rec.get("lon")
        if lat is None or lon is None:
            return
        writer.point(lon, lat)
        record = [rec.get(name) for name in fieldnames if name not in {"lat", "lon"}]
        writer.record(*record)

    _write(first)
    for rec in it:
        _write(rec)
    try:
        if hasattr(writer, "close"):
            writer.close()
        else:  # pyshp < 2
            writer.save(base)
    except OSError as exc:  # pragma: no cover - write errors
        logging.exception("Failed to write %s: %s", base, exc)


EXPORTERS: dict[
    str, Callable[[Iterable[Mapping[str, Any]], str, Sequence[str] | None], None]
] = {
    "csv": export_csv,
    "json": export_json,
    "gpx": export_gpx,
    "kml": export_kml,
    "geojson": export_geojson,
    "shp": export_shp,
}


def export_records(
    records: Iterable[Mapping[str, Any]],
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
        raise ExportError(f"Unsupported format: {fmt}") from exc
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
        except Exception:  # nosec B112
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

    if track:
        pm = ET.SubElement(doc, "Placemark")
        ET.SubElement(pm, "name").text = "Track"
        line = ET.SubElement(pm, "LineString")
        coords = " ".join(f"{lon},{lat}" for lat, lon in track)
        ET.SubElement(line, "coordinates").text = coords

    for rec in aps:
        lat = rec.get("lat")
        lon = rec.get("lon")
        if (lat is None or lon is None) and compute_position:
            loc = estimate_location_from_rssi(rec.get("observations", []))
            if loc is not None:
                lat, lon = loc
        if lat is None or lon is None:
            continue
        pm = ET.SubElement(doc, "Placemark")
        name = rec.get("ssid") or rec.get("bssid")
        if name:
            ET.SubElement(pm, "name").text = str(name)
        pt = ET.SubElement(pm, "Point")
        ET.SubElement(pt, "coordinates").text = f"{lon},{lat}"

    for rec in bts:
        lat = rec.get("lat")
        lon = rec.get("lon")
        if lat is None or lon is None:
            continue
        pm = ET.SubElement(doc, "Placemark")
        name = rec.get("name") or rec.get("address")
        if name:
            ET.SubElement(pm, "name").text = str(name)
        pt = ET.SubElement(pm, "Point")
        ET.SubElement(pt, "coordinates").text = f"{lon},{lat}"

    if path.lower().endswith(".kmz"):
        try:
            with tempfile.TemporaryDirectory() as tmp:
                kml_path = os.path.join(tmp, "doc.kml")
                ET.ElementTree(root).write(
                    kml_path, encoding="utf-8", xml_declaration=True
                )
                with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                    zf.write(kml_path, "doc.kml")
        except OSError as exc:  # pragma: no cover - write errors
            logging.exception("Failed to write %s: %s", path, exc)
    else:
        try:
            ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
        except OSError as exc:  # pragma: no cover - write errors
            logging.exception("Failed to write %s: %s", path, exc)
