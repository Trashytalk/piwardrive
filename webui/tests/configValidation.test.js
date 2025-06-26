import { describe, it, expect, vi } from 'vitest';
import fs from 'fs';
import os from 'os';
import path from 'path';

function setupTemp() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'cfg-'));
  const orig = process.cwd();
  process.chdir(dir);
  vi.resetModules();
  const cfg = require('../src/config.js');
  process.chdir(orig);
  return cfg;
}

describe('config validation', () => {
  it('invalid env value', () => {
    const cfg = setupTemp();
    process.env.PW_MAP_POLL_GPS = '0';
    process.env.PW_GPS_MOVEMENT_THRESHOLD = '-1';
    expect(() => cfg.AppConfig.load()).toThrow();
  });

  it('invalid theme', () => {
    const cfg = setupTemp();
    process.env.PW_THEME = 'Blue';
    expect(() => cfg.AppConfig.load()).toThrow();
  });
});
