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

import { execSync as _execSync } from 'child_process';

export function scanImsis(cmd, { execSync = _execSync, getPosition = () => null } = {}) {
  const output = execSync(cmd, { encoding: 'utf8' });
  const records = output.trim().split('\n').filter(Boolean).map(line => {
    const [imsi='', mcc='', mnc='', rssi=''] = line.split(',').map(p => p.trim());
    return { imsi, mcc, mnc, rssi };
  });
  const pos = getPosition();
  if (pos) {
    const [lat, lon] = pos;
    records.forEach(r => {
      r.lat = lat;
      r.lon = lon;
    });
  }
  return applyPostProcessors('imsi', records);
}
