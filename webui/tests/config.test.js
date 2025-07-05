import { describe, it, expect, vi, afterEach } from 'vitest';
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
  return { dir, cfg };
}

function clearEnv() {
  for (const key of Object.keys(process.env)) {
    if (key.startsWith('PW_')) delete process.env[key];
  }
}

describe('config helpers', () => {
  afterEach(() => {
    clearEnv();
  });

  it('loads defaults when missing', () => {
    const { cfg } = setupTemp();
    const data = cfg.loadConfig();
    expect(data.theme).toBe(cfg.DEFAULT_CONFIG.theme);
    expect(data.map_poll_gps).toBe(cfg.DEFAULT_CONFIG.map_poll_gps);
    expect(data.map_poll_bt).toBe(cfg.DEFAULT_CONFIG.map_poll_bt);
  });

  it('save and load roundtrip', () => {
    const { cfg } = setupTemp();
    const orig = cfg.loadConfig();
    orig.theme = 'Light';
    orig.map_poll_gps = 5;
    orig.map_poll_bt = 30;
    cfg.saveConfig(orig);
    const loaded = cfg.loadConfig();
    expect(loaded.theme).toBe('Light');
    expect(loaded.map_poll_gps).toBe(5);
    expect(loaded.map_poll_bt).toBe(30);
  });

  it('env override integer', () => {
    const { cfg } = setupTemp();
    process.env.PW_MAP_POLL_GPS = '42';
    const app = cfg.AppConfig.load();
    expect(app.map_poll_gps).toBe(42);
  });

  it('env override boolean', () => {
    const { cfg } = setupTemp();
    process.env.PW_MAP_SHOW_BT = 'true';
    const app = cfg.AppConfig.load();
    expect(app.map_show_bt).toBe(true);
  });

  it('list env overrides', () => {
    const { cfg } = setupTemp();
    const mapping = cfg.listEnvOverrides();
    expect(mapping['PW_UI_FONT_SIZE']).toBe('ui_font_size');
  });

  it('export and import json', () => {
    const { cfg, dir } = setupTemp();
    const file = path.join(dir, 'out.json');
    cfg.exportConfig({ theme: 'Green' }, file);
    const loaded = cfg.importConfig(file);
    expect(loaded.theme).toBe('Green');
  });

  it('export and import yaml', () => {
    const { cfg, dir } = setupTemp();
    const file = path.join(dir, 'out.yaml');
    cfg.exportConfig({ theme: 'Red' }, file);
    const loaded = cfg.importConfig(file);
    expect(loaded.theme).toBe('Red');
  });

  it('profile roundtrip', () => {
    const { cfg, dir } = setupTemp();
    const profileName = 'alt';
    const data = { theme: 'Green' };
    cfg.saveConfig(data, profileName);
    cfg.setActiveProfile('alt');
    const loaded = cfg.loadConfig();
    expect(loaded.theme).toBe('Green');
    expect(cfg.listProfiles()).toContain('alt');
  });

  it('import and export profile', () => {
    const { cfg, dir } = setupTemp();
    const src = path.join(dir, 'src.json');
    fs.writeFileSync(src, '{"theme": "Light"}');
    const name = cfg.importProfile(src);
    expect(name).toBe('src');
    const exported = path.join(dir, 'exp.json');
    cfg.exportProfile(name, exported);
    expect(fs.existsSync(exported)).toBe(true);
  });

  it('save config validation error', () => {
    const { cfg } = setupTemp();
    expect(() =>
      cfg.saveConfig({ ...cfg.DEFAULT_CONFIG, map_poll_gps: 0 })
    ).toThrow();
  });

  it('config mtime updates', () => {
    const { cfg } = setupTemp();
    const c = { ...cfg.DEFAULT_CONFIG };
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
