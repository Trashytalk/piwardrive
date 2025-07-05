import crypto from 'crypto';
import path from 'path';

/* global Buffer */

export function sanitizePath(p) {
  const normalized = path.normalize(p);
  if (normalized.split(path.sep).includes('..')) {
    throw new Error('Unsafe path');
  }
  return normalized;
}

export function validateServiceName(name) {
  if (!/^[\w.-]+$/.test(name)) {
    throw new Error('Invalid service name');
  }
}

export function hashPassword(password) {
  const salt = crypto.randomBytes(16);
  const digest = crypto.pbkdf2Sync(password, salt, 100000, 32, 'sha256');
  return Buffer.concat([salt, digest]).toString('base64');
}

export function verifyPassword(password, hashed) {
  try {
    const data = Buffer.from(hashed, 'base64');
    const salt = data.slice(0, 16);
    const digest = data.slice(16);
    const check = crypto.pbkdf2Sync(password, salt, 100000, 32, 'sha256');
    return crypto.timingSafeEqual(check, digest);
  } catch {
    return false;
  }
}
