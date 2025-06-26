export function parseImsiOutput(output) {
  const records = [];
  for (const line of output.split(/\n/)) {
    if (!line) continue;
    const parts = line.split(',').map(p => p.trim());
    const [imsi, mcc = '', mnc = '', rssi = ''] = parts;
    records.push({ imsi, mcc, mnc, rssi, lat: null, lon: null });
  }
  return records;
}

export function parseBandOutput(output) {
  const records = [];
  for (const line of output.split(/\n/)) {
    if (!line) continue;
    const parts = line.split(',').map(p => p.trim());
    if (parts.length >= 3) {
      const [band, channel, rssi] = parts;
      records.push({ band, channel, rssi });
    }
  }
  return records;
}
