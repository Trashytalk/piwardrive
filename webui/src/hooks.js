const _POST_PROCESSORS = {};

export function registerPostProcessor(type, func) {
  if (!_POST_PROCESSORS[type]) _POST_PROCESSORS[type] = [];
  _POST_PROCESSORS[type].push(func);
}

export function applyPostProcessors(type, records) {
  const funcs = _POST_PROCESSORS[type] || [];
  let out = records.slice();
  for (const fn of funcs) {
    try {
      out = Array.from(fn(out));
    } catch (_) {
      // ignore errors
    }
  }
  return out;
}

export function resetHooks() {
  for (const k of Object.keys(_POST_PROCESSORS)) delete _POST_PROCESSORS[k];
}
