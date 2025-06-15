import json
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
    if fmt == "csv":
        rows = list(records)
        if not rows:
            open(path, "w", encoding="utf-8").close()
        else:
            fieldnames = fields or list(rows[0].keys())
            with open(path, "w", encoding="utf-8", newline="") as fh:
                writer = csv.DictWriter(fh, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
    elif fmt == "json":
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(list(records), fh)
    elif fmt == "gpx":
        root = ET.Element("gpx", version="1.1", creator="piwardrive")
        for rec in records:
            lat = rec.get("lat")
            lon = rec.get("lon")
            if lat is None or lon is None:
                continue
            wpt = ET.SubElement(root, "wpt", lat=str(lat), lon=str(lon))
            name = rec.get("ssid") or rec.get("bssid")
            if name:
                ET.SubElement(wpt, "name").text = str(name)
        ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    elif fmt == "kml":
        root = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
        doc = ET.SubElement(root, "Document")
        for rec in records:
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
    else:  # pragma: no cover - safety net
        raise ValueError(fmt)
