import { describe, it, expect } from 'vitest';
import { computeSecurityScore } from '../src/securityAnalytics.js';

describe('computeSecurityScore', () => {
  it('computes weighted score', () => {
    const score = computeSecurityScore({
      networkScore: 80,
      encryptionStrength: 90,
      threatLevel: 70,
      configIssues: ['a', 'b'],
    });
    expect(score).toBe(70); // 32 + 27 + 21 - 10 = 70
  });

  it('clamps to range', () => {
    expect(computeSecurityScore({ networkScore: 200 })).toBe(100);
    expect(computeSecurityScore({ networkScore: -10 })).toBe(0);
  });
});
