export function suggestRoute(
  points,
  cellSize = 0.001,
  steps = 5,
  searchRadius = 5
) {
  const pts = points.map((p) => [Number(p[0]), Number(p[1])]);
  if (pts.length === 0) return [];
  const toCell = (lat, lon) => [
    Math.floor(lat / cellSize),
    Math.floor(lon / cellSize),
  ];
  const visited = new Set(pts.map((p) => toCell(p[0], p[1]).join(',')));
  let cur = toCell(pts[pts.length - 1][0], pts[pts.length - 1][1]);
  const route = [];
  for (let i = 0; i < steps; i++) {
    let best = null;
    let bestDist = null;
    for (let dx = -searchRadius; dx <= searchRadius; dx++) {
      for (let dy = -searchRadius; dy <= searchRadius; dy++) {
        const cell = [cur[0] + dx, cur[1] + dy];
        const key = cell.join(',');
        if (visited.has(key)) continue;
        const dist = dx * dx + dy * dy;
        if (bestDist === null || dist < bestDist) {
          best = cell;
          bestDist = dist;
        }
      }
    }
    if (!best) break;
    visited.add(best.join(','));
    cur = best;
    const lat = (best[0] + 0.5) * cellSize;
    const lon = (best[1] + 0.5) * cellSize;
    route.push([lat, lon]);
  }
  return route;
}
