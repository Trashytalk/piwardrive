const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const ex = require('../scripts/exportLogs.js');

test('writes logs and uploads', async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'logs-'));
  const log = path.join(tmp, 'app.log');
  fs.writeFileSync(log, '1\n2\n3');
  let uploaded = null;
  const res = await ex.run(
    [
      '--lines',
      '2',
      '--upload',
      'http://remote',
      '--output',
      path.join(tmp, 'out.txt'),
    ],
    {
      defaultLogPath: () => log,
      uploadFile: async (file, url) => {
        uploaded = { file, url };
      },
    }
  );
  assert.ok(fs.existsSync(path.join(tmp, 'out.txt')));
  const out = fs.readFileSync(path.join(tmp, 'out.txt'), 'utf8');
  assert.equal(out, '2\n3');
  assert.deepStrictEqual(uploaded.url, 'http://remote');
  assert.deepStrictEqual(res, { uploaded: true });
});

test('returns path when not uploading', async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'logs-'));
  const log = path.join(tmp, 'app.log');
  fs.writeFileSync(log, 'a\nb\nc');
  const res = await ex.run(['-n', '1', '--output', path.join(tmp, 'out.txt')], {
    defaultLogPath: () => log,
  });
  assert.equal(res.path.endsWith('out.txt'), true);
  const out = fs.readFileSync(res.path, 'utf8');
  assert.equal(out, 'c');
});
