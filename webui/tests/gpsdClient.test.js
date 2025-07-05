import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

var mockSocket;
vi.mock('net', async () => {
  const { EventEmitter } = await import('events');
  mockSocket = new EventEmitter();
  mockSocket.write = vi.fn();
  mockSocket.destroy = vi.fn();
  return {
    createConnection: vi.fn(() => {
      setTimeout(() => mockSocket.emit('connect'), 0);
      return mockSocket;
    }),
  };
});
import { getFix } from '../src/gpsdClient.js';
import * as net from 'net';

vi.useFakeTimers();

describe('gpsdClient getFix', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    mockSocket.write.mockClear();
    mockSocket.destroy.mockClear();
  });

  afterEach(() => {
    vi.clearAllTimers();
    vi.useRealTimers();
  });

  it('returns TPV data when available', async () => {
    const promise = getFix(100);
    await vi.advanceTimersByTimeAsync(0);
    mockSocket.emit(
      'data',
      Buffer.from('{"class":"TPV","lat":1,"lon":2,"mode":3}\n')
    );
    const data = await promise;
    expect(data.lat).toBe(1);
    expect(mockSocket.write).toHaveBeenCalled();
  });

  it('returns null on timeout', async () => {
    const promise = getFix(50);
    await vi.advanceTimersByTimeAsync(60);
    const data = await promise;
    expect(data).toBeNull();
    expect(mockSocket.destroy).toHaveBeenCalled();
  });
});
