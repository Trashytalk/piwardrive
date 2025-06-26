import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import fs from 'fs';
import path from 'path';

const tmpRoot = path.join(process.cwd(), 'tmp_plugin');
const pluginDir = path.join(tmpRoot, '.config', 'piwardrive', 'plugins');
let mod;

function setupEnv() {
  fs.rmSync(tmpRoot, { recursive: true, force: true });
  fs.mkdirSync(pluginDir, { recursive: true });
  process.env.HOME = tmpRoot;
}

describe('widgetPlugins', () => {
  beforeEach(() => {
    setupEnv();
    fs.writeFileSync(path.join(pluginDir, 'plug1.js'), 'exports.Widget1 = function(){}');
    mod = require('../src/widgetPlugins.js');
  });

  afterEach(() => {
    fs.rmSync(tmpRoot, { recursive: true, force: true });
    delete require.cache[require.resolve('../src/widgetPlugins.js')];
  });

  it('discovers plugins', () => {
    const names = mod.listPlugins();
    expect(names).toContain('Widget1');
    expect(typeof mod.getPlugin('Widget1')).toBe('function');
  });

  it('clears cache and reloads', () => {
    mod.listPlugins();
    fs.writeFileSync(path.join(pluginDir, 'plug2.js'), 'exports.Widget2 = function(){}');
    mod.clearPluginCache();
    const names = mod.listPlugins();
    expect(names).toContain('Widget2');
  });
});
