"""Parsers for cellular data output."""

from typing import List, Dict


def parse_band_output(output: str) -> List[Dict[str, str]]:
    """Parse band scanner CSV ``output`` into a list of dictionaries."""
    records: List[Dict[str, str]] = []
    for line in output.splitlines():
        parts = [p.strip() for p in line.split(',')]
        if len(parts) >= 3:
            band, channel, rssi = parts[:3]
            records.append({'band': band, 'channel': channel, 'rssi': rssi})
    return records


def parse_imsi_output(output: str) -> List[Dict[str, str]]:
    """Parse IMSI catcher CSV ``output`` into a list of dictionaries."""
    records: List[Dict[str, str]] = []
    for line in output.splitlines():
        parts = [p.strip() for p in line.split(',')]
        if not parts:
            continue
        imsi = parts[0]
        mcc = parts[1] if len(parts) > 1 else ''
        mnc = parts[2] if len(parts) > 2 else ''
        rssi = parts[3] if len(parts) > 3 else ''
        records.append({'imsi': imsi, 'mcc': mcc, 'mnc': mnc, 'rssi': rssi})
    return records

__all__ = ['parse_band_output', 'parse_imsi_output']
