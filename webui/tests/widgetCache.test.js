import { describe, it, expect, vi } from 'vitest';
import { loadPlugins, clearCache, _cache } from '../src/widgetCache.js';

const modules = {
  './components/TestWidget.jsx': vi.fn(async () => ({ default: () => 'plug' })),
};

describe('widget cache', () => {
  it('caches loaded plugins', async () => {
    await loadPlugins(['TestWidget'], modules);
    expect(modules['./components/TestWidget.jsx']).toHaveBeenCalledTimes(1);
    await loadPlugins(['TestWidget'], modules);
    expect(modules['./components/TestWidget.jsx']).toHaveBeenCalledTimes(1);
    expect(_cache.TestWidget).toBeDefined();
    clearCache();
    await loadPlugins(['TestWidget'], modules);
    expect(modules['./components/TestWidget.jsx']).toHaveBeenCalledTimes(2);
  });
});
