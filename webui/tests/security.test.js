import { describe, it, expect } from 'vitest';
import { hashPassword, verifyPassword, sanitizePath, validateServiceName } from '../src/security.js';

describe('security helpers', () => {
  it('hashes and verifies password', () => {
    const h = hashPassword('secret');
    expect(verifyPassword('secret', h)).toBe(true);
    expect(verifyPassword('wrong', h)).toBe(false);
  });

  it('validates service name', () => {
    expect(() => validateServiceName('good.service')).not.toThrow();
    expect(() => validateServiceName('../bad')).toThrow();
  });

  it('sanitizes valid path', () => {
    const p = 'a/b/../c.txt';
    expect(sanitizePath(p)).toBe(require('path').normalize(p));
  });

  ['../etc/passwd', 'a/../../secret.txt'].forEach(p => {
    it(`rejects unsafe path ${p}`, () => {
      expect(() => sanitizePath(p)).toThrow();
    });
  });
});
