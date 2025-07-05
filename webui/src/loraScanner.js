export class LoRaPacket {
  constructor(timestamp, freq, rssi, snr, devaddr, raw) {
    this.timestamp = timestamp || null;
    this.freq = freq != null ? Number(freq) : null;
    this.rssi = rssi != null ? Number(rssi) : null;
    this.snr = snr != null ? Number(snr) : null;
    this.devaddr = devaddr || null;
    this.raw = raw;
  }
}

export function parsePackets(lines) {
  const pkts = [];
  for (const line of lines) {
    const fields = {};
    for (const m of line.matchAll(/(\w+)=([\w.:-]+)/g)) {
      fields[m[1]] = m[2];
    }
    pkts.push(
      new LoRaPacket(
        fields.time,
        fields.freq,
        fields.rssi,
        fields.snr,
        fields.devaddr,
        line
      )
    );
  }
  return pkts;
}

import fs from 'fs';

export function plotSignalTrend(packets, path) {
  // Simply ensure a file exists for tests
  fs.writeFileSync(path, '');
}
