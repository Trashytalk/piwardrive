const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('path');
const { spawnSync } = require('child_process');
const { createServer } = require('../server/index.js');

function getOrientationMap() {
  const script =
    'import json, piwardrive.orientation_sensors as os; print(json.dumps(os.clone_orientation_map()))';
  const proc = spawnSync('python3', ['-c', script], {
    encoding: 'utf8',
    env: { ...process.env, PYTHONPATH: path.join(__dirname, '..', 'src') },
  });
  if (proc.status !== 0) {
    throw new Error(proc.stderr.trim() || 'failed');
  }
  return JSON.parse(proc.stdout);
}

test('orientation map endpoint returns current map', async () => {
  process.env.PYTHONPATH = path.join(__dirname, '..', 'src');
  const app = createServer();
  const server = app.listen(0);
  const url = `http://127.0.0.1:${server.address().port}/api/orientation-map`;
  try {
    const res = await fetch(url);
    assert.equal(res.status, 200);
    const data = await res.json();
    const expected = getOrientationMap();
    assert.deepStrictEqual(data, expected);
  } finally {
    server.close();
  }
});
