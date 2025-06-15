from typing import List, Tuple

def parse_coords(text: str) -> List[Tuple[float, float]]:
    """Parse a KML coordinates string into ``(lat, lon)`` tuples."""
    coords = []
    for pair in text.strip().split():
        try:
            parts = pair.split(',')
            lon = float(parts[0])
            lat = float(parts[1])
        except Exception:
            coords.append((0.0, 0.0))
        else:
            coords.append((lat, lon))
    return coords
