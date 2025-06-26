import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import LogViewer from '../src/components/LogViewer.jsx';

vi.useFakeTimers();
let origInterval;
let origClear;
let intervalFn;

describe('LogViewer', () => {
  beforeEach(() => {
    origInterval = global.setInterval;
    origClear = global.clearInterval;
    global.setInterval = (fn) => { intervalFn = fn; fn(); return 1; };
    global.clearInterval = () => { intervalFn = null; };
  });

  afterEach(() => {
    vi.clearAllTimers();
    vi.restoreAllMocks();
    global.setInterval = origInterval;
    global.clearInterval = origClear;
  });

  it('calls fetch with params', async () => {
    global.fetch = vi.fn(() => Promise.resolve({ json: () => Promise.resolve({ lines: ['A', 'B'] }) }));
    const { unmount } = render(<LogViewer path="/a.log" lines={10} />);
    await Promise.resolve();
    expect(global.fetch).toHaveBeenCalledWith('/logs?path=%2Fa.log&lines=10');
    unmount();
  });

  it('polls periodically', async () => {
    let count = 0;
    global.fetch = vi.fn(() => Promise.resolve({ json: () => Promise.resolve({ lines: [`L${++count}`] }) }));
    const { unmount } = render(<LogViewer />);
    await Promise.resolve();
    expect(global.fetch).toHaveBeenCalledTimes(2);
    intervalFn();
    await Promise.resolve();
    expect(global.fetch).toHaveBeenCalledTimes(3);
    unmount();
  });
});
