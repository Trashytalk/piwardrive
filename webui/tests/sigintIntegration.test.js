import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import fs from 'fs';
import path from 'path';
import { loadSigintData } from '../src/sigintIntegration.js';

let origDir;

describe('sigint integration', () => {
  beforeEach(() => {
    origDir = process.env.SIGINT_EXPORT_DIR;
  });
  afterEach(() => {
    if (origDir === undefined) delete process.env.SIGINT_EXPORT_DIR;
    else process.env.SIGINT_EXPORT_DIR = origDir;
  });

  it('returns records from json file', () => {
    const dir = fs.mkdtempSync(path.join(process.cwd(), 'tmp-'));
    const data = [{ a: 1 }, { b: 2 }];
    fs.writeFileSync(path.join(dir, 'wifi.json'), JSON.stringify(data));
    process.env.SIGINT_EXPORT_DIR = dir;
    expect(loadSigintData('wifi')).toEqual(data);
  });

  it('handles missing file', () => {
    const dir = fs.mkdtempSync(path.join(process.cwd(), 'tmp-'));
    process.env.SIGINT_EXPORT_DIR = dir;
    expect(loadSigintData('wifi')).toEqual([]);
  });
});
