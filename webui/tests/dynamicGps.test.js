import { describe, it, expect } from 'vitest';
import { adjustGpsInterval } from '../src/dynamicGps.js';

describe('adjustGpsInterval', () => {
  it('doubles interval when stationary', () => {
    const cfg = { poll: 5, max: 20, thresh: 1.0 };
    expect(adjustGpsInterval(5, 0.5, cfg.poll, cfg.max, cfg.thresh)).toBe(10);
    expect(adjustGpsInterval(10, 0.5, cfg.poll, cfg.max, cfg.thresh)).toBe(20);
    expect(adjustGpsInterval(20, 0.5, cfg.poll, cfg.max, cfg.thresh)).toBe(20);
  });

  it('resets interval on movement', () => {
    const cfg = { poll: 5, max: 20, thresh: 1.0 };
    expect(adjustGpsInterval(20, 2.0, cfg.poll, cfg.max, cfg.thresh)).toBe(5);
  });
});
