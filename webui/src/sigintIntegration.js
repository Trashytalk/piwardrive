import fs from 'fs';
import path from 'path';

/* global process */
import { EXPORT_DIR } from './sigintPaths.js';

export function loadSigintData(name) {
  const exportDir = process.env.SIGINT_EXPORT_DIR || EXPORT_DIR;
  const file = path.join(exportDir, `${name}.json`);
  try {
    const text = fs.readFileSync(file, 'utf-8');
    const data = JSON.parse(text);
    if (Array.isArray(data)) {
      return data
        .filter(r => typeof r === 'object' && r !== null)
        .map(r => ({ ...r }));
    }
  } catch {
    // ignore missing or invalid files
  }
  return [];
}
