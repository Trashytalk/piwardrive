import { execFileSync, execFile } from 'child_process';

export function parseTowerOutput(output) {
  const records = [];
  for (const line of output.split(/\n+/)) {
    if (!line) continue;
    const parts = line.split(',').map((p) => p.trim());
    if (parts.length >= 2) {
      const [tower_id, rssi] = parts;
      records.push({ tower_id, rssi, lat: null, lon: null });
    }
  }
  return records;
}

export function scanTowers(cmd = 'tower-scan', timeout) {
  try {
    const out = execFileSync(cmd, {
      encoding: 'utf-8',
      timeout: timeout ? timeout * 1000 : undefined,
    });
    return parseTowerOutput(out);
  } catch {
    return [];
  }
}

export function asyncScanTowers(cmd = 'tower-scan', timeout) {
  return new Promise((resolve) => {
    execFile(
      cmd,
      { encoding: 'utf-8', timeout: timeout ? timeout * 1000 : undefined },
      (err, stdout) => {
        if (err) {
          resolve([]);
          return;
        }
        resolve(parseTowerOutput(stdout));
      }
    );
  });
}
