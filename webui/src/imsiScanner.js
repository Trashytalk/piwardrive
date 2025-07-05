export const _postProcessors = {};

export function registerPostProcessor(type, fn) {
  if (!_postProcessors[type]) _postProcessors[type] = [];
  _postProcessors[type].push(fn);
}

export function clearPostProcessors(type) {
  _postProcessors[type] = [];
}

function applyPostProcessors(type, records) {
  const procs = _postProcessors[type] || [];
  return procs.reduce((recs, fn) => fn(recs), records);
}

import { execSync as _execSync, execFile } from 'child_process';
import { getFix } from './gpsdClient.js';

export function parseImsiOutput(output) {
  return output
    .trim()
    .split('\n')
    .filter(Boolean)
    .map((line) => {
      const [imsi = '', mcc = '', mnc = '', rssi = ''] = line
        .split(',')
        .map((p) => p.trim());
      return { imsi, mcc, mnc, rssi };
    });
}

export function scanImsis(
  cmd,
  { execSync = _execSync, getPosition = () => null } = {}
) {
  const output = execSync(cmd, { encoding: 'utf8' });
  const records = parseImsiOutput(output);
  const pos = getPosition();
  if (pos) {
    const [lat, lon] = pos;
    records.forEach((r) => {
      r.lat = lat;
      r.lon = lon;
    });
  }
  return applyPostProcessors('imsi', records);
}

export function asyncScanImsis(
  cmd,
  { execFileFunc = execFile, getFixFunc = getFix, timeout } = {}
) {
  return new Promise((resolve) => {
    execFileFunc(
      cmd,
      { encoding: 'utf8', timeout: timeout ? timeout * 1000 : undefined },
      async (err, stdout) => {
        if (err) {
          resolve([]);
          return;
        }
        const records = parseImsiOutput(stdout);
        const fix = await getFixFunc();
        if (fix && fix.lat != null && fix.lon != null) {
          records.forEach((r) => {
            r.lat = fix.lat;
            r.lon = fix.lon;
          });
        }
        resolve(applyPostProcessors('imsi', records));
      }
    );
  });
}
