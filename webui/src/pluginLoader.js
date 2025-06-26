export async function loadPluginComponents(names, modules) {
  const loaded = [];
  for (const name of names) {
    const path = `./components/${name}.jsx`;
    const importer = modules[path];
    if (importer) {
      try {
        const mod = await importer();
        loaded.push({ name, Component: mod.default });
      } catch {
        // ignore failed import
      }
    }
  }
  return loaded;
}
