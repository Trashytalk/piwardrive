#!/usr/bin/env node
// Simple health probe for the PiWardrive server.
// Performs an HTTP request to /api/status and exits non-zero on failure.

async function run(argv = process.argv.slice(2), helpers = {}) {
  const opts = { fetch: global.fetch, ...helpers };
  let url = 'http://127.0.0.1:8000';
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--url') url = argv[++i];
  }
  if (!url.endsWith('/')) url += '/';
  const target = url + 'api/status';
  const resp = await opts.fetch(target);
  if (!resp.ok) throw new Error(`status ${resp.status}`);
  return true;
}

if (require.main === module) {
  run().catch((err) => {
    console.error(err.message);
    process.exit(1);
  });
}

module.exports = { run };
