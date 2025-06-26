import { describe, it, expect, beforeEach } from 'vitest';
import { registerPostProcessor, applyPostProcessors, resetHooks } from '../src/hooks.js';

describe('hooks', () => {
  beforeEach(() => resetHooks());

  it('applies processors', () => {
    registerPostProcessor('wifi', recs => recs.map(r => ({ ...r, extra: true })));
    const out = applyPostProcessors('wifi', [{ ssid: 'a' }]);
    expect(out[0].extra).toBe(true);
  });
});
