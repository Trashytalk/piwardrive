const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { createServer } = require('../server/index.js');

function tmpFile() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'srv-'));
  return { dir, file: path.join(dir, 'health.json') };
}

test('serves contents from PW_HEALTH_FILE', async () => {
  const { dir, file } = tmpFile();
  fs.writeFileSync(file, JSON.stringify([{ timestamp: 'ts1' }]));
  process.env.PW_HEALTH_FILE = file;
  const app = createServer();
  const server = app.listen(0);
  const url = `http://127.0.0.1:${server.address().port}/api/status`;
  try {
    const res = await fetch(url);
    assert.equal(res.status, 200);
    const data = await res.json();
    assert.deepStrictEqual(data, [{ timestamp: 'ts1' }]);
  } finally {
    server.close();
    fs.rmSync(dir, { recursive: true, force: true });
    delete process.env.PW_HEALTH_FILE;
  }
});

function loadWidgets() {
  const script = path.join(__dirname, '..', 'server', 'parse_widgets.py');
  const file = path.join(__dirname, '..', 'src', 'piwardrive', 'widgets', '__init__.py');
  const { spawnSync } = require('child_process');
  const proc = spawnSync('python3', [script, file], { encoding: 'utf8' });
  if (proc.status !== 0) throw new Error(proc.stderr.trim() || 'failed');
  return JSON.parse(proc.stdout);
}

test('serves widget list', async () => {
  const app = createServer();
  const server = app.listen(0);
  const url = `http://127.0.0.1:${server.address().port}/api/widgets`;
  try {
    const res = await fetch(url);
    assert.equal(res.status, 200);
    const data = await res.json();
    assert.deepStrictEqual(data.widgets, loadWidgets());
  } finally {
    server.close();
  }
});
