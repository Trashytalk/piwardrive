const express = require('express');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

function verifyPassword(password, hashed) {
  try {
    const data = Buffer.from(hashed, 'base64');
    const salt = data.slice(0, 16);
    const digest = data.slice(16);
    const check = crypto.pbkdf2Sync(
      password,
      salt,
      100000,
      digest.length,
      'sha256'
    );
    return crypto.timingSafeEqual(check, digest);
  } catch {
    return false;
  }
}

function basicAuth(req, res, next) {
  const pwHash = process.env.PW_API_PASSWORD_HASH;
  if (!pwHash) return next();
  const header = req.headers.authorization || '';
  if (!header.startsWith('Basic ')) {
    res.set('WWW-Authenticate', 'Basic');
    return res.status(401).end();
  }
  const decoded = Buffer.from(header.slice(6), 'base64').toString();
  const password = decoded.split(':')[1] || '';
  if (!verifyPassword(password, pwHash)) {
    res.set('WWW-Authenticate', 'Basic');
    return res.status(401).end();
  }
  next();
}

let widgetCache = null;
let widgetStamp = 0;

function parseWidgets() {
  const file = path.join(
    __dirname,
    '..',
    'src',
    'piwardrive',
    'widgets',
    '__init__.py'
  );
  const script = path.join(__dirname, 'parse_widgets.py');

  try {
    const mtime = fs.statSync(file).mtimeMs;
    if (widgetCache && widgetStamp === mtime) {
      return widgetCache;
    }
  } catch {
    // ignore stat errors and regenerate cache
  }

  try {
    const { spawnSync } = require('child_process');
    const proc = spawnSync('python3', [script, file], { encoding: 'utf8' });
    if (proc.status !== 0) {
      throw new Error(proc.stderr.trim() || 'failed');
    }
    const data = JSON.parse(proc.stdout);
    if (!Array.isArray(data) || !data.every((w) => typeof w === 'string')) {
      throw new Error('invalid widget data');
    }
    widgetCache = data;
    try {
      widgetStamp = fs.statSync(file).mtimeMs;
    } catch {
      widgetStamp = 0;
    }
    return widgetCache;
  } catch {
    widgetCache = [];
    widgetStamp = 0;
    return widgetCache;
  }
}

function createServer(opts = {}) {
  const distDir =
    opts.distDir ||
    process.env.PW_WEBUI_DIST ||
    path.join(__dirname, '..', 'webui', 'dist');
  const healthFile = opts.healthFile || process.env.PW_HEALTH_FILE;
  const app = express();

  app.use('/api', basicAuth);
  app.use(express.static(distDir));

  function loadHealth() {
    if (!healthFile) return [];
    try {
      return JSON.parse(fs.readFileSync(healthFile, 'utf8'));
    } catch {
      return [];
    }
  }

  app.get('/api/status', (req, res) => {
    res.json(loadHealth());
  });

  app.get('/api/widgets', (req, res) => {
    res.json({ widgets: parseWidgets() });
  });

  app.get('/api/orientation-map', (req, res) => {
    const script =
      'import json, piwardrive.orientation_sensors as os; print(json.dumps(os.clone_orientation_map()))';
    try {
      const { spawnSync } = require('child_process');
      const proc = spawnSync('python3', ['-c', script], { encoding: 'utf8' });
      if (proc.status !== 0) {
        throw new Error(proc.stderr.trim() || 'failed');
      }
      res.json(JSON.parse(proc.stdout));
    } catch (err) {
      res.status(500).json({ error: 'orientation map unavailable' });
    }
  });

  return app;
}

if (require.main === module) {
  const port = process.env.PORT || 8000;
  createServer().listen(port, () => {
    console.log(`Server listening on ${port}`);
  });
}

module.exports = { createServer };
