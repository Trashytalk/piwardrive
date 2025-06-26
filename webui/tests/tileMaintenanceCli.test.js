import { describe, it, expect } from 'vitest';
import { runCli } from './tileMaintenanceCli.js';

describe('tile maintenance CLI', () => {
  it('parses args and calls maintenance functions', () => {
    const result = runCli([
      '--purge',
      '--limit',
      '--vacuum',
      '--offline',
      'db.mbtiles',
      '--folder',
      'cache',
      '--max-age-days',
      '1',
      '--limit-mb',
      '2',
    ]);
    expect(result).toEqual({
      purge: ['cache', 1],
      limit: ['cache', 2],
      vacuum: 'db.mbtiles',
    });
  });
});
