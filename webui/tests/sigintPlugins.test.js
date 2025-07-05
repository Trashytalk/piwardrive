import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import fs from 'fs';
import path from 'path';
import { getPlugin, clearPluginCache } from '../src/sigintPlugins.js';

let origHome;

describe('sigint plugins', () => {
  beforeEach(() => {
    origHome = process.env.HOME;
  });
  afterEach(() => {
    process.env.HOME = origHome;
    clearPluginCache();
  });

  it('loads plugin module', () => {
    const tmp = fs.mkdtempSync(path.join(process.cwd(), 'tmp-'));
    const dir = path.join(tmp, '.config', 'piwardrive', 'sigint_plugins');
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(
      path.join(dir, 'example.js'),
      'module.exports.scan = () => [{id:1}];'
    );
    process.env.HOME = tmp;
    clearPluginCache();
    const mod = getPlugin('example');
    expect(mod.scan()).toEqual([{ id: 1 }]);
  });

  it('ignores broken plugin', () => {
    const tmp = fs.mkdtempSync(path.join(process.cwd(), 'tmp-'));
    const dir = path.join(tmp, '.config', 'piwardrive', 'sigint_plugins');
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, 'bad.js'), 'throw new Error("boom")');
    process.env.HOME = tmp;
    clearPluginCache();
    const mod = getPlugin('bad');
    expect(mod).toBeUndefined();
  });
});
