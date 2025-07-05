import { describe, it, expect } from 'vitest';
import { parseJson, parseCsv } from '../src/healthImport.js';

describe('parseJson', () => {
  it('parses records', async () => {
    const txt = JSON.stringify([
      {
        timestamp: 't',
        cpu_temp: 1,
        cpu_percent: 2,
        memory_percent: 3,
        disk_percent: 4,
      },
    ]);
    const recs = await parseJson(txt);
    expect(recs[0].cpu_percent).toBe(2);
  });
});

describe('parseCsv', () => {
  it('parses records', async () => {
    const csv =
      'timestamp,cpu_temp,cpu_percent,memory_percent,disk_percent\n' +
      't,1,2,3,4';
    const recs = await parseCsv(csv);
    expect(recs[0].memory_percent).toBe(3);
  });
});
