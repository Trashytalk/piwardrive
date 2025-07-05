export async function parseJson(text) {
  const data = JSON.parse(text);
  const out = [];
  for (const row of data) {
    if (typeof row !== 'object') continue;
    out.push({
      timestamp: String(row.timestamp || ''),
      cpu_temp: row.cpu_temp ?? null,
      cpu_percent: Number(row.cpu_percent || 0),
      memory_percent: Number(row.memory_percent || 0),
      disk_percent: Number(row.disk_percent || 0),
    });
  }
  return out;
}

export async function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/);
  const [headerLine, ...rows] = lines;
  const headers = headerLine.split(',');
  const out = [];
  for (const line of rows) {
    if (!line) continue;
    const cols = line.split(',');
    const rec = {};
    headers.forEach((h, i) => {
      rec[h] = cols[i];
    });
    out.push({
      timestamp: rec.timestamp || '',
      cpu_temp: rec.cpu_temp ? Number(rec.cpu_temp) : null,
      cpu_percent: Number(rec.cpu_percent || 0),
      memory_percent: Number(rec.memory_percent || 0),
      disk_percent: Number(rec.disk_percent || 0),
    });
  }
  return out;
}
