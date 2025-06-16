import json
import os
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from typing import Any, Iterable, Mapping, Sequence

import csv

EXPORT_FORMATS = ("csv", "json", "gpx", "kml")


def filter_records(
    records: Iterable[Mapping[str, Any]],
    ssid: str | None = None,
    encryption: str | None = None,
    oui: str | None = None,
) -> list[dict[str, Any]]:
    """Return records matching optional SSID, encryption or OUI filters."""
    result: list[dict[str, Any]] = []
    for rec in records:
        if ssid and ssid not in (rec.get("ssid") or ""):
            continue
        if encryption and encryption != rec.get("encryption"):
            continue
        if oui and not (rec.get("bssid") or "").startswith(oui):
            continue
        result.append(dict(rec))
    return result


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
    if fmt not in EXPORT_FORMATS:
        raise ValueError(f"Unsupported format: {fmt}")

    def export_csv(
        rows: Sequence[Mapping[str, Any]],
        p: str,
        f: Sequence[str] | None,
    ) -> None:
        rows = list(rows)
        with open(p, "w", newline="", encoding="utf-8") as fh:
            if rows:
                fieldnames = f or list(rows[0].keys())
                writer = csv.DictWriter(fh, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

    def export_json(
        rs: Sequence[Mapping[str, Any]],
        p: str,
        _f: Sequence[str] | None,
    ) -> None:
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(list(rs), fh)

    def export_gpx(
        rs: Sequence[Mapping[str, Any]],
        p: str,
        _f: Sequence[str] | None,
    ) -> None:
        root = ET.Element("gpx", version="1.1", creator="piwardrive")
        for rec in rs:
            lat = rec.get("lat")
            lon = rec.get("lon")
            if lat is None or lon is None:
                continue
            wpt = ET.SubElement(root, "wpt", lat=str(lat), lon=str(lon))
            name = rec.get("ssid") or rec.get("bssid")
            if name:
                ET.SubElement(wpt, "name").text = str(name)
        ET.ElementTree(root).write(p, encoding="utf-8", xml_declaration=True)

    def export_kml(
        rs: Sequence[Mapping[str, Any]],
        p: str,
        _f: Sequence[str] | None,
    ) -> None:
        root = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
        doc = ET.SubElement(root, "Document")
        for rec in rs:
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
        ET.ElementTree(root).write(p, encoding="utf-8", xml_declaration=True)

    exporters = {
        "csv": export_csv,
        "json": export_json,
        "gpx": export_gpx,
        "kml": export_kml,
    }

    try:
        exporter = exporters[fmt]
    except KeyError as exc:  # pragma: no cover - safety net
        raise ValueError(f"Unsupported format: {fmt}") from exc
    exporter(records, path, fields)


def estimate_location_from_rssi(points: Sequence[Mapping[str, float]]) -> tuple[float, float] | None:
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
        with tempfile.TemporaryDirectory() as tmp:
            kml_path = os.path.join(tmp, "doc.kml")
            ET.ElementTree(root).write(kml_path, encoding="utf-8", xml_declaration=True)
            with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                zf.write(kml_path, "doc.kml")
    else:
        ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)

