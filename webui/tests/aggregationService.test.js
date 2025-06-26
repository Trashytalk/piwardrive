// @vitest-environment node
import { describe, it, beforeAll, afterAll, expect } from 'vitest';
import fs from 'fs';
import os from 'os';
import path from 'path';
import { spawn, execSync } from 'child_process';

const PORT = 9101; // use different port to avoid conflict

function createDb(dbPath) {
  const cmds = [
    "CREATE TABLE health_records (timestamp TEXT PRIMARY KEY, cpu_temp REAL, cpu_percent REAL, memory_percent REAL, disk_percent REAL);",
    "CREATE TABLE ap_cache (bssid TEXT, ssid TEXT, encryption TEXT, lat REAL, lon REAL, last_time INTEGER);",
    "INSERT INTO health_records VALUES ('t1', 40.0, 10.0, 50.0, 20.0);",
    "INSERT INTO health_records VALUES ('t2', 50.0, 20.0, 40.0, 30.0);",
    "INSERT INTO ap_cache VALUES ('b','s','wpa',1.0,2.0,0);",
    "INSERT INTO ap_cache VALUES ('c','s','wpa',1.1,2.1,0);"
  ];
  execSync(`sqlite3 ${dbPath} \"${cmds.join('')}\"`);
}

async function waitForServer() {
  for (let i = 0; i < 20; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${PORT}/stats`);
      if (r.ok) return;
    } catch {}
    await new Promise(res => setTimeout(res, 200));
  }
  throw new Error('server not ready');
}

describe('aggregation service', () => {
  let proc; let tmpDir; let dbPath;

  beforeAll(async () => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'agg-'));
    dbPath = path.join(tmpDir, 'upload.db');
    createDb(dbPath);
    proc = spawn('python', [path.join('tests', 'run_agg_server.py')], {
      cwd: path.join(__dirname, '..'),
      env: { ...process.env, PORT: String(PORT), PW_AGG_DIR: tmpDir, PYTHONPATH: path.join('..', 'src') },
      stdio: 'inherit'
    });
    await waitForServer();
  });

  afterAll(() => {
    if (proc) proc.kill();
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('uploads DB and returns stats', async () => {
    const fd = new FormData();
    const buf = fs.readFileSync(dbPath);
    fd.append('file', new Blob([buf]), 'db');
    const upload = await fetch(`http://127.0.0.1:${PORT}/upload`, { method: 'POST', body: fd });
    expect(upload.status).toBe(200);

    const statsResp = await fetch(`http://127.0.0.1:${PORT}/stats`);
    const stats = await statsResp.json();
    expect(Math.round(stats.temp_avg * 10) / 10).toBe(45.0);
    expect(stats.cpu_avg).toBe(15.0);

    const overlayResp = await fetch(`http://127.0.0.1:${PORT}/overlay?bins=1`);
    const overlay = await overlayResp.json();
    expect(overlay.points[0][2]).toBe(2);
  });

  it('appends uploads to existing file', async () => {
    const dest = path.join(tmpDir, 'uploads', 'db');
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.writeFileSync(dest, 'x');

    const fd = new FormData();
    const buf = fs.readFileSync(dbPath);
    fd.append('file', new Blob([buf]), 'db');
    const resp = await fetch(`http://127.0.0.1:${PORT}/upload`, { method: 'POST', body: fd });
    expect(resp.status).toBe(200);
    const size = fs.statSync(dest).size;
    expect(size).toBeGreaterThan(1);
  });
});
