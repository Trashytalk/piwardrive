import { describe, it, expect } from 'vitest';
import { kalman1d } from '../src/kalman.js';

function variance(arr) {
  const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
  return arr.reduce((s, x) => s + (x - mean) ** 2, 0) / arr.length;
}

function randomSeries(n, seed = 1) {
  let x = seed;
  const arr = [];
  for (let i = 0; i < n; i++) {
    x = (x * 16807) % 2147483647;
    arr.push((x / 2147483646) - 0.5);
  }
  return arr;
}

describe('kalman1d', () => {
  it('reduces variance', () => {
    const data = randomSeries(100, 1);
    const filtered = kalman1d(data, 0.0001, 0.01);
    expect(filtered.length).toBe(data.length);
    expect(Math.abs(filtered[0] - data[0]) < 1e-9).toBe(true);
    expect(variance(filtered)).toBeLessThan(variance(data));
  });
});
