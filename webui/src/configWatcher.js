export function watchConfig(url = '/config', onChange, interval = 2000) {
  let last = null;
  const load = async () => {
    try {
      const resp = await fetch(url);
      if (!resp.ok) return;
      const cfg = await resp.json();
      const j = JSON.stringify(cfg);
      if (j !== last) {
        last = j;
        onChange(cfg);
      }
    } catch (_) {
      /* ignore */
    }
  };
  load();
  const id = setInterval(load, interval);
  return () => clearInterval(id);
}
