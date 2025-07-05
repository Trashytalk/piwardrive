import { describe, it, expect } from 'vitest';
import fs from 'fs';
import os from 'os';
import path from 'path';
import {
  parsePackets,
  plotSignalTrend,
  LoRaPacket,
} from '../src/loraScanner.js';

describe('parsePackets', () => {
  it('parses lines', () => {
    const lines = [
      'time=2024-01-01T00:00:00Z freq=868.1 rssi=-120 snr=7.5 devaddr=ABC',
      'time=2024-01-01T00:00:01Z freq=868.1 rssi=-118 snr=6.8 devaddr=ABC',
    ];
    const packets = parsePackets(lines);
    expect(packets.length).toBe(2);
    expect(packets[0].freq).toBe(868.1);
    expect(packets[0].rssi).toBe(-120);
    expect(packets[0].devaddr).toBe('ABC');
  });
});

describe('plotSignalTrend', () => {
  it('creates a file', () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'lora-'));
    const out = path.join(tmpDir, 'trend.png');
    const packets = [
      new LoRaPacket('t1', 868.1, -120, 7.5, 'A', ''),
      new LoRaPacket('t2', 868.1, -118, 6.8, 'A', ''),
    ];
    plotSignalTrend(packets, out);
    expect(fs.existsSync(out)).toBe(true);
  });
});
