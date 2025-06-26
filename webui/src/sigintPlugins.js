import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);

function pluginDir() {
  return path.join(process.env.HOME || '', '.config', 'piwardrive', 'sigint_plugins');
}
let PLUGIN_STAMP = null;
const PLUGINS = {};

function loadPlugins() {
  let stat;
  const dir = pluginDir();
  try {
    stat = fs.statSync(dir);
  } catch {
    return;
  }
  const stamp = stat.mtimeMs;
  if (PLUGIN_STAMP !== stamp) {
    for (const k in PLUGINS) delete PLUGINS[k];
  }
  for (const file of fs.readdirSync(dir)) {
    const full = path.join(dir, file);
    if (fs.statSync(full).isFile() && file.endsWith('.js')) {
      try {
        const mod = require(full);
        PLUGINS[path.basename(file, '.js')] = mod;
      } catch {
        // ignore broken plugin
      }
    }
  }
  PLUGIN_STAMP = stamp;
}

export function getPlugin(name) {
  loadPlugins();
  return PLUGINS[name];
}

export function clearPluginCache() {
  PLUGIN_STAMP = null;
  for (const k in PLUGINS) delete PLUGINS[k];
}
