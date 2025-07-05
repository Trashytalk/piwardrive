import { execFileSync, execFile } from 'child_process';

export function parseBandOutput(output) {
  const records = [];
  output.split(/\n+/).forEach((line) => {
    const parts = line.split(',').map((p) => p.trim());
    if (parts.length >= 3) {
      const [band, channel, rssi] = parts;
      records.push({ band, channel, rssi });
    }
  });
  return records;
}

export function scanBands(cmd = 'celltrack', timeout) {
  try {
    const out = execFileSync(cmd, {
      encoding: 'utf-8',
      timeout: timeout ? timeout * 1000 : undefined,
    });
    return parseBandOutput(out);
  } catch (err) {
    return [];
  }
}

export function asyncScanBands(cmd = 'celltrack', timeout) {
  return new Promise((resolve) => {
    execFile(
      cmd,
      { encoding: 'utf-8', timeout: timeout ? timeout * 1000 : undefined },
      (err, stdout) => {
        if (err) {
          resolve([]);
          return;
        }
        resolve(parseBandOutput(stdout));
      }
    );
  });
}
