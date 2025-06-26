import { loadPlugins } from './widgetCache.js';

export async function loadPluginComponents(names, modules) {
  return loadPlugins(names, modules);
}
