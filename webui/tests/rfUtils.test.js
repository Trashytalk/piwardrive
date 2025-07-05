import { describe, it, expect } from 'vitest';
import { spectrumScan, demodulateFm } from '../src/rfUtils.js';

describe('rfUtils', () => {
  it('spectrumScan returns freq and power arrays', () => {
    const [freqs, power] = spectrumScan(100, { sampleRate: 4, numSamples: 4 });
    expect(freqs.length).toBe(4);
    expect(power.length).toBe(4);
    expect(freqs[0]).toBeCloseTo(98);
  });

  it('demodulateFm returns expected constant', () => {
    const audio = demodulateFm(100, {
      sampleRate: 8,
      audioRate: 2,
      duration: 1,
    });
    expect(audio.length).toBe(2);
    audio.forEach((val) => {
      expect(Math.abs(val - Math.PI / 2)).toBeLessThan(1e-6);
    });
  });
});
