import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { healthSummary, setRpy2Available } from '../src/rIntegration.js';

describe('rIntegration health summary', () => {
  let origFetch;
  beforeEach(() => {
    origFetch = global.fetch;
  });
  afterEach(() => {
    global.fetch = origFetch;
    setRpy2Available(true);
  });

  it('throws when rpy2 is missing', async () => {
    setRpy2Available(false);
    await expect(healthSummary('data.csv')).rejects.toThrow('rpy2 is required');
  });

  it('summarizes without plot', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({ text: () => Promise.resolve('1\n2\n3') })
    );
    const result = await healthSummary('file.csv');
    expect(result).toEqual({ average: 2 });
  });

  it('summarizes with plot path', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({ text: () => Promise.resolve('2\n4') })
    );
    const result = await healthSummary('file.csv', 'out.png');
    expect(result).toEqual({ average: 3, plot: 'out.png' });
  });
});
