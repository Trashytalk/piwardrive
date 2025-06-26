// @vitest-environment node
import { describe, it, beforeAll, afterAll, expect } from 'vitest';
import fs from 'fs';
import os from 'os';
import path from 'path';
import crypto from 'crypto';
import { createServer } from '../../server/index.js';

const PORT = 9123;
let server;
let tmpDir;
let healthFile;
let distDir;

function hashPassword(password) {
  const salt = crypto.randomBytes(16);
  const digest = crypto.pbkdf2Sync(password, salt, 100000, 32, 'sha256');
  return Buffer.concat([salt, digest]).toString('base64');
}

beforeAll(() => {
  tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'srv-'));
  distDir = path.join(tmpDir, 'dist');
  fs.mkdirSync(distDir);
  fs.writeFileSync(path.join(distDir, 'index.html'), '<h1>hello</h1>');
  healthFile = path.join(tmpDir, 'health.json');
  fs.writeFileSync(healthFile, JSON.stringify([{ timestamp: 't1' }]));
  process.env.PW_API_PASSWORD_HASH = hashPassword('pw');
  server = createServer({ distDir, healthFile }).listen(PORT);
});

afterAll(() => {
  server.close();
  fs.rmSync(tmpDir, { recursive: true, force: true });
  delete process.env.PW_API_PASSWORD_HASH;
});

describe('node server', () => {
  it('serves static files', async () => {
    const res = await fetch(`http://127.0.0.1:${PORT}/`);
    expect(res.status).toBe(200);
    expect(await res.text()).toContain('hello');
  });

  it('requires auth for API', async () => {
    const res = await fetch(`http://127.0.0.1:${PORT}/api/status`);
    expect(res.status).toBe(401);
  });

  it('returns health records with auth', async () => {
    const hdr = 'Basic ' + Buffer.from('u:pw').toString('base64');
    const res = await fetch(`http://127.0.0.1:${PORT}/api/status`, {
      headers: { Authorization: hdr },
    });
    const data = await res.json();
    expect(data[0].timestamp).toBe('t1');
  });

  it('lists widgets', async () => {
    const hdr = 'Basic ' + Buffer.from('u:pw').toString('base64');
    const res = await fetch(`http://127.0.0.1:${PORT}/api/widgets`, {
      headers: { Authorization: hdr },
    });
    const data = await res.json();
    expect(Array.isArray(data.widgets)).toBe(true);
    expect(data.widgets.length).toBeGreaterThan(0);
  });
});
