import { describe, it, expect } from 'vitest';
import { formatError, pointInPolygon } from '../src/utils.js';

describe('formatError', () => {
  it('formats message', () => {
    expect(formatError('E1', 'fail')).toBe('[E1] fail');
  });
});

describe('pointInPolygon', () => {
  it('detects containment', () => {
    const poly = [
      [0, 0],
      [0, 1],
      [1, 1],
      [1, 0],
    ];
    expect(pointInPolygon([0.5, 0.5], poly)).toBe(true);
    expect(pointInPolygon([1.5, 0.5], poly)).toBe(false);
  });
});
