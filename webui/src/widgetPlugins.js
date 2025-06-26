import fs from 'fs';
import path from 'path';

const PLUGIN_DIR = path.join(process.env.HOME || '', '.config', 'piwardrive', 'plugins');
let PLUGIN_STAMP = null;
const PLUGINS = {};

function loadPlugins() {
  let stat;
  try {
    stat = fs.statSync(PLUGIN_DIR);
  } catch {
    return;
  }
  const stamp = stat.mtimeMs;
  if (PLUGIN_STAMP === stamp && Object.keys(PLUGINS).length) return;
  if (PLUGIN_STAMP !== stamp) {
    for (const k in PLUGINS) delete PLUGINS[k];
  }
  for (const file of fs.readdirSync(PLUGIN_DIR)) {
    const full = path.join(PLUGIN_DIR, file);
    if (fs.statSync(full).isFile() && /\.(js|mjs|cjs)$/i.test(file)) {
      try {
        const mod = require(full);
        for (const [name, obj] of Object.entries(mod)) {
          if (typeof obj === 'function') {
            PLUGINS[name] = obj;
          }
        }
      } catch {}
    }
  }
  PLUGIN_STAMP = stamp;
}

export function listPlugins() {
  loadPlugins();
  return Object.keys(PLUGINS);
}

export function getPlugin(name) {
  loadPlugins();
  return PLUGINS[name];
}

export function clearPluginCache() {
  PLUGIN_STAMP = null;
  for (const k in PLUGINS) delete PLUGINS[k];
}
