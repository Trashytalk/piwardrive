export const _cache = {};

export async function loadPlugins(names = [], modules = {}) {
  const loaded = [];
  for (const name of names) {
    if (name in _cache) {
      loaded.push({ name, Component: _cache[name] });
      continue;
    }
    const importer = modules[`./components/${name}.jsx`];
    if (importer) {
      try {
        const mod = await importer();
        _cache[name] = mod.default;
        loaded.push({ name, Component: mod.default });
      } catch {
        // ignore failed import
      }
    }
  }
  return loaded;
}

export function clearCache() {
  for (const key in _cache) delete _cache[key];
}
