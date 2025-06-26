import { describe, it, expect } from 'vitest';
import { suggestRoute } from '../src/routeOptimizer.js';

describe('suggestRoute', () => {
  it('returns empty list for empty input', () => {
    expect(suggestRoute([])).toEqual([]);
  });

  it('suggests unvisited cells', () => {
    const points = [
      [0.0, 0.0],
      [0.0, 0.001],
      [0.0, 0.002]
    ];
    const route = suggestRoute(points, 0.001, 2, 1);
    const visited = new Set(points.map(([lat, lon]) => `${Math.floor(lat/0.001)},${Math.floor(lon/0.001)}`));
    expect(route.length).toBeLessThanOrEqual(2);
    for (const [lat, lon] of route) {
      const cell = `${Math.floor(lat/0.001)},${Math.floor(lon/0.001)}`;
      expect(visited.has(cell)).toBe(false);
    }
  });
});
