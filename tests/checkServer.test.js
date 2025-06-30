const test = require('node:test');
const assert = require('node:assert/strict');
const { run } = require('../scripts/check_server.js');

test('run resolves when server healthy', async () => {
  const origFetch = global.fetch;
  let called = null;
  global.fetch = async (url) => {
    called = url;
    return { ok: true, status: 200 };
  };
  try {
    const res = await run(['--url', 'http://example']);
    assert.strictEqual(res, true);
    assert.strictEqual(called, 'http://example/api/status');
  } finally {
    global.fetch = origFetch;
  }
});

test('run rejects on failure status', async () => {
  const origFetch = global.fetch;
  global.fetch = async () => ({ ok: false, status: 500 });
  try {
    await run(['--url', 'http://example']);
    assert.fail('should throw');
  } catch (err) {
    assert.ok(err instanceof Error);
  } finally {
    global.fetch = origFetch;
  }
});
