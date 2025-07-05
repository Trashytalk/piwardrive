const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { watchConfig } = require('../scripts/configWatcher.js');

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

test('watchConfig triggers on change', async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'cfg-'));
  const file = path.join(dir, 'config.json');
  fs.writeFileSync(file, '{}');
  let triggered = false;
  const watcher = watchConfig(file, () => {
    triggered = true;
  });
  try {
    await sleep(100);
    fs.writeFileSync(file, '{"a":1}');
    for (let i = 0; i < 20 && !triggered; i++) {
      await sleep(100);
    }
  } finally {
    watcher.close();
  }
  assert.ok(triggered);
});
