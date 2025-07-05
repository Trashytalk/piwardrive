#!/usr/bin/env node
// Minimal utility for syncing a database file and reporting service status.
// Usage: node serviceSync.js --db path --url url --services svc1 svc2

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

async function uploadDb(dbPath, url) {
  const data = fs.readFileSync(dbPath);
  const form = new FormData();
  form.append('file', new Blob([data]), path.basename(dbPath));
  const resp = await fetch(url, { method: 'POST', body: form });
  if (!resp.ok) throw new Error(`upload failed: ${resp.status}`);
  return true;
}

function checkStatus(service) {
  try {
    execSync(`systemctl is-active --quiet ${service}`);
    return true;
  } catch {
    return false;
  }
}

function parseArgs(argv) {
  const args = { services: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--db') args.db = argv[++i];
    else if (a === '--url') args.url = argv[++i];
    else if (a === '--services') {
      while (argv[i + 1] && !argv[i + 1].startsWith('--')) {
        args.services.push(argv[++i]);
      }
    }
  }
  return args;
}

async function run(argv = process.argv.slice(2), helpers = {}) {
  const opts = { uploadDb, checkStatus, ...helpers };

  const args = parseArgs(argv);

  if ((args.db && !args.url) || (!args.db && args.url)) {
    throw new Error('db and url must be provided together');
  }

  const result = {};

  if (args.services.length) {
    result.status = {};
    for (const svc of args.services) {
      result.status[svc] = opts.checkStatus(svc);
    }
  }

  if (args.db && args.url) {
    await opts.uploadDb(args.db, args.url);
    result.synced = true;
  }

  return result;
}

if (require.main === module) {
  run()
    .then((r) => {
      console.log(JSON.stringify(r));
    })
    .catch((err) => {
      console.error(err.message);
      process.exit(1);
    });
}

module.exports = { run, uploadDb, checkStatus };
