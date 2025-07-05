import { describe, it, expect } from 'vitest';
import { parseCoords } from '../src/ckml.js';

describe('parseCoords', () => {
  it('parses simple coordinates', () => {
    const coords = parseCoords('1,2 3,4');
    expect(coords).toEqual([
      [2, 1],
      [4, 3],
    ]);
  });

  it('parses coordinates with altitude', () => {
    const coords = parseCoords('1,2,3 4,5,6');
    expect(coords).toEqual([
      [2, 1],
      [5, 4],
    ]);
  });

  it('parses negative coordinates', () => {
    const coords = parseCoords('-1,-2 -3,-4');
    expect(coords).toEqual([
      [-2, -1],
      [-4, -3],
    ]);
  });

  it('handles malformed token', () => {
    const coords = parseCoords('foo');
    expect(coords).toEqual([[0, 0]]);
  });

  it('handles mixed valid and invalid', () => {
    const coords = parseCoords('1,2 foo 3,4');
    expect(coords).toEqual([
      [2, 1],
      [0, 0],
      [4, 3],
    ]);
  });
});
