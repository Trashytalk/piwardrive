"""Python fallback implementation for ckml extension."""


def parse_coords(text: str) -> list[tuple[float, float]]:
    """Parse a KML ``coordinates`` string into ``(lat, lon)`` tuples."""
    coords: list[tuple[float, float]] = []
    for pair in text.strip().split():
        parts = pair.split(",")
        if len(parts) < 2:
            coords.append((0.0, 0.0))
            continue
        lon = float(parts[0])
        lat = float(parts[1])
        coords.append((lat, lon))

    return coords
