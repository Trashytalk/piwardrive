import { describe, it, expect, vi } from 'vitest';
import { parseTowerOutput, scanTowers, asyncScanTowers } from '../src/towerScanner.js';
import * as childProcess from 'child_process';

vi.mock('child_process');

describe('parseTowerOutput', () => {
  it('parses lines', () => {
    const out = '123,-70\n456,-80';
    const rec = parseTowerOutput(out);
    expect(rec).toEqual([
      { tower_id: '123', rssi: '-70', lat: null, lon: null },
      { tower_id: '456', rssi: '-80', lat: null, lon: null },
    ]);
  });
});

describe('scanTowers', () => {
  it('executes command', () => {
    const spy = vi.spyOn(childProcess, 'execFileSync').mockReturnValue('123,-70');
    const res = scanTowers('dummy');
    expect(spy).toHaveBeenCalled();
    expect(res.length).toBe(1);
    spy.mockRestore();
  });
});

describe('asyncScanTowers', () => {
  it('returns records', async () => {
    vi.spyOn(childProcess, 'execFile').mockImplementation((cmd, opts, cb) => {
      cb(null, '123,-70');
    });
    const res = await asyncScanTowers('dummy');
    expect(res).toEqual([{ tower_id: '123', rssi: '-70', lat: null, lon: null }]);
  });
});
