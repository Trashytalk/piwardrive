import { execFileSync, execFile } from 'child_process';
import { getHeading } from './orientationSensors.js';
import { cachedLookupVendor } from './ouiRegistry.js';
import { reportError } from './exceptionHandler.js';

export function parseIwlist(output) {
  const records = [];
  let current = null;
  let encLines = [];
  const lines = output.split(/\n+/);
  for (const line of lines) {
    const l = line.trim();
    if (l.startsWith('Cell')) {
      if (current) {
        if (encLines.length) {
          current.encryption = (
            (current.encryption || '') +
            ' ' +
            encLines.join(' ')
          ).trim();
        }
        records.push(current);
      }
      current = { cell: l };
      const addrMatch = l.match(/Address:\s*([A-Fa-f0-9:]+)/);
      if (addrMatch) current.bssid = addrMatch[1];
      encLines = [];
    } else if (l.includes('ESSID')) {
      current.ssid = l.split(':', 2)[1].replace(/"/g, '').trim();
    } else if (l.startsWith('Frequency')) {
      current.frequency = l.split('Frequency:')[1].split(' ')[0];
      const chMatch = l.match(/Channel\s*(\d+)/);
      if (chMatch) current.channel = chMatch[1];
    } else if (l.startsWith('Channel:')) {
      current.channel = l.split('Channel:')[1].trim();
    } else if (l.startsWith('Encryption key:')) {
      current.encryption = l.split('Encryption key:')[1].trim();
    } else if (l.startsWith('IE:')) {
      encLines.push(l.split('IE:')[1].trim());
    } else if (l.includes('Quality=')) {
      current.quality = l.split('Quality=')[1].split(' ')[0];
    }
  }
  if (current) {
    if (encLines.length) {
      current.encryption = (
        (current.encryption || '') +
        ' ' +
        encLines.join(' ')
      ).trim();
    }
    records.push(current);
  }
  return records.map((r) => {
    const vendor = r.bssid ? cachedLookupVendor(r.bssid) : null;
    const heading = getHeading();
    if (vendor) r.vendor = vendor;
    if (heading != null) r.heading = heading;
    return r;
  });
}

export function scanWifi(
  iface = 'wlan0',
  iwlistCmd = 'iwlist',
  privCmd = 'sudo',
  timeout
) {
  try {
    const args = [];
    if (privCmd) args.push(...privCmd.split(/\s+/));
    args.push(iwlistCmd, iface, 'scanning');
    const out = execFileSync(args[0], args.slice(1), {
      encoding: 'utf-8',
      timeout: timeout ? timeout * 1000 : undefined,
      stdio: ['ignore', 'pipe', 'ignore'],
    });
    return parseIwlist(out);
  } catch (e) {
    reportError(e);
    return [];
  }
}

export function asyncScanWifi(
  iface = 'wlan0',
  iwlistCmd = 'iwlist',
  privCmd = 'sudo',
  timeout
) {
  return new Promise((resolve) => {
    const args = [];
    if (privCmd) args.push(...privCmd.split(/\s+/));
    args.push(iwlistCmd, iface, 'scanning');
    execFile(
      args[0],
      args.slice(1),
      {
        encoding: 'utf-8',
        timeout: timeout ? timeout * 1000 : undefined,
        stdio: ['ignore', 'pipe', 'ignore'],
      },
      (err, stdout) => {
        if (err) {
          resolve([]);
          return;
        }
        resolve(parseIwlist(stdout));
      }
    );
  });
}
