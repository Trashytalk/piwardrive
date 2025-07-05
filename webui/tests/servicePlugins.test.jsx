import { describe, it, expect, vi } from 'vitest';
import { loadPluginComponents } from '../src/pluginLoader.js';

const modules = {
  './components/TestPlugin.jsx': vi.fn(async () => ({ default: () => 'plug' })),
};

describe('plugin loader', () => {
  it('loads components by name', async () => {
    const loaded = await loadPluginComponents(['TestPlugin'], modules);
    expect(modules['./components/TestPlugin.jsx']).toHaveBeenCalled();
    expect(loaded[0].name).toBe('TestPlugin');
  });
});
