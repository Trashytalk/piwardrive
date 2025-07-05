import fs from 'fs';

export function exportJson(records, path) {
  fs.writeFileSync(path, JSON.stringify(records, null, 2));
}

export function exportCsv(records, path) {
  if (!records.length) {
    fs.writeFileSync(path, '');
    return;
  }
  const keys = Object.keys(records[0]);
  const lines = [keys.join(',')];
  for (const rec of records) {
    lines.push(keys.map((k) => String(rec[k])).join(','));
  }
  fs.writeFileSync(path, lines.join('\n'));
}

export function exportYaml(records, path) {
  const lines = records.map(
    (r) =>
      '-\n' +
      Object.entries(r)
        .map(([k, v]) => `  ${k}: ${v}`)
        .join('\n')
  );
  fs.writeFileSync(path, lines.join('\n'));
}
