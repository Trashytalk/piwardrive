import { describe, it, expect } from 'vitest';
import fs from 'fs';
import { exportJson, exportCsv, exportYaml } from '../src/sigintExporter.js';
import { tmpdir } from 'os';
import { join } from 'path';

describe('sigint exporter', () => {
  it('writes json', () => {
    const path = join(tmpdir(), 'data.json');
    const records = [{ a: 1 }];
    exportJson(records, path);
    const data = JSON.parse(fs.readFileSync(path, 'utf-8'));
    expect(data).toEqual(records);
    fs.unlinkSync(path);
  });

  it('writes csv', () => {
    const path = join(tmpdir(), 'data.csv');
    const records = [{ a: '1', b: '2' }];
    exportCsv(records, path);
    const text = fs.readFileSync(path, 'utf-8').trim();
    expect(text).toBe('a,b\n1,2');
    fs.unlinkSync(path);
  });

  it('writes yaml', () => {
    const path = join(tmpdir(), 'data.yaml');
    const records = [{ a: 1 }];
    exportYaml(records, path);
    const text = fs.readFileSync(path, 'utf-8');
    expect(text).toContain('a: 1');
    fs.unlinkSync(path);
  });
});

it('exports include exportYaml', async () => {
  const mod = await import('../src/sigintExporter.js');
  expect('exportYaml' in mod).toBe(true);
});
