import { describe, it, expect, vi, afterEach } from 'vitest';
import fs from 'fs';
import { setupLogging } from '../src/logconfig.js';
import path from 'path';

function tmpFile(name) {
  return path.join(process.cwd(), name);
}

describe('setupLogging', () => {
  afterEach(() => {
    delete process.env.PW_LOG_LEVEL;
  });

  it('writes JSON', () => {
    const file = tmpFile('log.json');
    if (fs.existsSync(file)) fs.unlinkSync(file);
    const logger = setupLogging({ logFile: file });
    logger.info('hello');
    const data = JSON.parse(fs.readFileSync(file, 'utf8'));
    expect(data.message).toBe('hello');
    expect(data.level).toBe('INFO');
    fs.unlinkSync(file);
  });

  it('respects env', () => {
    process.env.PW_LOG_LEVEL = 'DEBUG';
    const file = tmpFile('log_env.json');
    if (fs.existsSync(file)) fs.unlinkSync(file);
    const logger = setupLogging({ logFile: file });
    logger.debug('hi');
    const data = JSON.parse(fs.readFileSync(file, 'utf8'));
    expect(data.level).toBe('DEBUG');
    expect(logger.level).toBe(10);
    fs.unlinkSync(file);
  });

  it('writes to stdout', () => {
    const file = tmpFile('log_out.json');
    if (fs.existsSync(file)) fs.unlinkSync(file);
    const write = vi
      .spyOn(process.stdout, 'write')
      .mockImplementation(() => {});
    const logger = setupLogging({ logFile: file, stdout: true });
    logger.warning('stream me');
    const data = JSON.parse(fs.readFileSync(file, 'utf8'));
    expect(data.message).toBe('stream me');
    expect(write).toHaveBeenCalled();
    write.mockRestore();
    fs.unlinkSync(file);
  });
});
