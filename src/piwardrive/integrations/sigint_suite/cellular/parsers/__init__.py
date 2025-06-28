"""Parsers for cellular data output."""

from typing import List

from piwardrive.sigint_suite.models import BandRecord, ImsiRecord, TowerRecord


def parse_band_output(output: str) -> List[BandRecord]:
    """Parse band scanner CSV ``output`` into :class:`BandRecord` objects."""
    records: List[BandRecord] = []
    for line in output.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 3:
            band, channel, rssi = parts[:3]
            records.append(BandRecord(band=band, channel=channel, rssi=rssi))
    return records


def parse_imsi_output(output: str) -> List[ImsiRecord]:
    """Parse IMSI catcher CSV ``output`` into :class:`ImsiRecord` objects."""
    records: List[ImsiRecord] = []
    for line in output.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if not parts:
            continue
        imsi = parts[0]
        mcc = parts[1] if len(parts) > 1 else ""
        mnc = parts[2] if len(parts) > 2 else ""
        rssi = parts[3] if len(parts) > 3 else ""
        records.append(ImsiRecord(imsi=imsi, mcc=mcc, mnc=mnc, rssi=rssi))
    return records


def parse_tower_output(output: str) -> List[TowerRecord]:
    """Parse tower scan CSV ``output`` into :class:`TowerRecord` objects."""
    records: List[TowerRecord] = []
    for line in output.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 2:
            tower_id, rssi = parts[:2]
            lat = float(parts[2]) if len(parts) > 2 and parts[2] else None
            lon = float(parts[3]) if len(parts) > 3 and parts[3] else None
            records.append(TowerRecord(tower_id=tower_id, rssi=rssi, lat=lat, lon=lon))
    return records


__all__ = ["parse_band_output", "parse_imsi_output", "parse_tower_output"]
