import { describe, it, expect } from 'vitest';

it('EXPORT_DIR env override', async () => {
  process.env.EXPORT_DIR = '/tmp/x';
  const { EXPORT_DIR } = await import('../src/sigintPaths.js');
  expect(EXPORT_DIR).toBe('/tmp/x');
  delete process.env.EXPORT_DIR;
});
