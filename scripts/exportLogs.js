#!/usr/bin/env node
// Export recent log lines and optionally upload them.

const fs = require('fs');
const os = require('os');
const path = require('path');

function defaultLogPath() {
  return path.join(os.homedir(), '.config', 'piwardrive', 'app.log');
}

function tailLines(file, count) {
  const data = fs.readFileSync(file, 'utf8').split('\n');
  return data.slice(-count).join('\n');
}

function saveLogs(lines, outPath) {
  fs.writeFileSync(outPath, lines, 'utf8');
  return outPath;
}

async function uploadFile(file, url) {
  const buf = fs.readFileSync(file);
  const form = new FormData();
  form.append('file', new Blob([buf]), path.basename(file));
  const resp = await fetch(url, { method: 'POST', body: form });
  if (!resp.ok) throw new Error(`upload failed: ${resp.status}`);
  return true;
}

function parseArgs(argv) {
  const args = { lines: 200 };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--output') args.output = argv[++i];
    else if (a === '--lines' || a === '-n') args.lines = parseInt(argv[++i], 10);
    else if (a === '--upload') args.upload = argv[++i];
  }
  return args;
}

async function run(argv = process.argv.slice(2), helpers = {}) {
  const opts = {
    defaultLogPath,
    tailLines,
    saveLogs,
    uploadFile,
    ...helpers,
  };

  const args = parseArgs(argv);

  const outPath = args.output || path.join(os.tmpdir(), `logs-${Date.now()}.txt`);
  const logPath = opts.defaultLogPath();
  const data = opts.tailLines(logPath, args.lines);
  opts.saveLogs(data, outPath);

  if (args.upload) {
    await opts.uploadFile(outPath, args.upload);
    return { uploaded: true };
  }
  return { path: outPath };
}

if (require.main === module) {
  run().then(r => {
    console.log(JSON.stringify(r));
  }).catch(err => {
    console.error(err.message);
    process.exit(1);
  });
}

module.exports = { run, tailLines, saveLogs, uploadFile, defaultLogPath };
