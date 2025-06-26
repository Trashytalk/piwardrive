import { describe, it } from 'vitest';
import fs from 'fs';
import path from 'path';

const srcDir = path.join(__dirname, '../src');
const MODULES = fs
  .readdirSync(srcDir)
  .filter((f) => (f.endsWith('.js') || f.endsWith('.jsx')) && f !== 'main.jsx')
  .map((f) => path.join('..', 'src', f));

describe('import top level modules', () => {
  for (const mod of MODULES) {
    it(`imports ${mod}`, async () => {
      await import(mod);
    });
  }
});
