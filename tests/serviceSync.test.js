const test = require('node:test');
const assert = require('node:assert/strict');
const svc = require('../scripts/serviceSync.js');

// helper to run run() and capture result

test('parses options and uploads', async () => {
  let uploaded = null;
  const res = await svc.run(
    ['--db', 'file.db', '--url', 'http://x', '--services', 'a', 'b'],
    {
      uploadDb: async (db, url) => {
        uploaded = { db, url };
      },
      checkStatus: () => true,
    }
  );
  assert.deepStrictEqual(uploaded, { db: 'file.db', url: 'http://x' });
  assert.deepStrictEqual(res, { synced: true, status: { a: true, b: true } });
});

test('errors when only db provided', async () => {
  try {
    await svc.run(['--db', 'only.db']);
    assert.fail('should throw');
  } catch (err) {
    assert.ok(err instanceof Error);
  }
});
