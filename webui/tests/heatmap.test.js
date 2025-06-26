import { describe, it, expect } from 'vitest';
import { histogram, histogramPoints, densityMap, coverageMap } from '../src/heatmap.js';

describe('histogram', () => {
  it('counts points', () => {
    const pts = [[0.1,0.1],[0.9,0.9],[0.8,0.8]];
    const [hist, lat, lon] = histogram(pts, 2, [0,0,1,1]);
    expect(lat).toEqual([0,1]);
    expect(lon).toEqual([0,1]);
    expect(hist[0][0]).toBe(1);
    expect(hist[1][1]).toBe(2);
  });
});

describe('histogramPoints', () => {
  it('returns centers', () => {
    const hist = [[0,1],[2,0]];
    const pts = histogramPoints(hist, [0,1], [0,1]);
    expect(pts.length).toBe(2);
    const values = pts.map(p => [Number(p[0].toFixed(1)), Number(p[1].toFixed(1)), p[2]]);
    const set = new Set(values.map(v => v.join(',')));
    expect(set.has('0.2,0.8,1') || set.has('0.8,0.2,2')).toBe(true);
  });
});

describe('densityMap', () => {
  it('expands counts', () => {
    const [dens] = densityMap([[0.5,0.5]], 3, [0,0,1,1], 1);
    const total = dens.reduce((a,row) => a + row.reduce((x,y)=>x+y,0), 0);
    expect(total).toBeGreaterThan(1);
  });
});

describe('coverageMap', () => {
  it('binary map', () => {
    const [cov] = coverageMap([[0.5,0.5]], 3, [0,0,1,1], 1);
    const flat = cov.flat();
    expect(flat.every(v => v===0||v===1)).toBe(true);
    expect(flat.reduce((a,b)=>a+b,0)).toBeGreaterThan(1);
  });
});
