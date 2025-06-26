const express = require('express');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

function verifyPassword(password, hashed) {
  try {
    const data = Buffer.from(hashed, 'base64');
    const salt = data.slice(0, 16);
    const digest = data.slice(16);
    const check = crypto.pbkdf2Sync(password, salt, 100000, digest.length, 'sha256');
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

function parseWidgets() {
  const file = path.join(__dirname, '..', 'src', 'piwardrive', 'widgets', '__init__.py');
  try {
    const text = fs.readFileSync(file, 'utf8');
    const start = text.indexOf('__all__');
    if (start === -1) return [];
    const section = text.slice(start, text.indexOf(']', start));
    return Array.from(section.matchAll(/"([^"]+)"/g)).map(m => m[1]);
  } catch {
    return [];
  }
}

function createServer(opts = {}) {
  const distDir = opts.distDir || path.join(__dirname, '..', 'webui', 'dist');
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

  return app;
}

if (require.main === module) {
  const port = process.env.PORT || 8000;
  createServer().listen(port, () => {
    console.log(`Server listening on ${port}`);
  });
}

module.exports = { createServer };
