export function parseCoords(text) {
  const result = [];
  for (const token of text.trim().split(/\s+/)) {
    const parts = token.split(',');
    if (parts.length < 2) {
      result.push([0, 0]);
      continue;
    }
    const lon = parseFloat(parts[0]);
    const lat = parseFloat(parts[1]);
    result.push([lat, lon]);
  }
  return result;
}
