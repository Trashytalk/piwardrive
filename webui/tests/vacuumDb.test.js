import { describe, it, expect, vi } from 'vitest';
import { main } from '../src/vacuumDb.js';
import * as childProcess from 'child_process';

describe('vacuumDb script', () => {
  it('calls sqlite3 vacuum', () => {
    const spy = vi.spyOn(childProcess, 'execFileSync').mockReturnValue(null);
    main('test.db');
    expect(spy).toHaveBeenCalledWith('sqlite3', ['test.db', 'VACUUM']);
    spy.mockRestore();
  });
});
