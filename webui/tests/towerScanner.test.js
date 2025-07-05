import { describe, it, expect, vi } from 'vitest';
vi.mock('child_process', () => {
  const execFileSync = vi.fn();
  const execFile = vi.fn();
  return { execFileSync, execFile, default: { execFileSync, execFile } };
});
import {
  parseTowerOutput,
  scanTowers,
  asyncScanTowers,
} from '../src/towerScanner.js';
import * as childProcess from 'child_process';

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
    childProcess.execFileSync.mockReturnValue('123,-70');
    const res = scanTowers('dummy');
    expect(childProcess.execFileSync).toHaveBeenCalled();
    expect(res.length).toBe(1);
  });
});

describe('asyncScanTowers', () => {
  it('returns records', async () => {
    childProcess.execFile.mockImplementation((cmd, opts, cb) => {
      cb(null, '123,-70');
    });
    const res = await asyncScanTowers('dummy');
    expect(res).toEqual([
      { tower_id: '123', rssi: '-70', lat: null, lon: null },
    ]);
    expect(childProcess.execFile).toHaveBeenCalled();
  });
});
