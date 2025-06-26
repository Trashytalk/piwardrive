import { describe, it, expect, vi } from 'vitest';
import fs from 'fs';
import os from 'os';
import path from 'path';

function setup() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'cfg-'));
  const orig = process.cwd();
  process.chdir(dir);
  vi.resetModules();
  const cfg = require('../src/config.js');
  process.chdir(orig);
  return cfg;
}

describe('config mtime', () => {
  it('updates on save', () => {
    const cfg = setup();
    const c = { ...cfg.DEFAULT_CONFIG, theme: 'Dark' };
    cfg.saveConfig(c);
    const first = cfg.configMtime();
    c.theme = 'Green';
    cfg.saveConfig(c);
    const second = cfg.configMtime();
    expect(first).not.toBeNull();
    expect(second).not.toBeNull();
    expect(second >= first).toBe(true);
  });
});
