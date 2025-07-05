import { render, screen, fireEvent, act } from '@testing-library/react';
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
    global.setInterval = (fn) => {
      intervalFn = fn;
      fn();
      return 1;
    };
    global.clearInterval = () => {
      intervalFn = null;
    };
  });

  afterEach(() => {
    vi.clearAllTimers();
    vi.restoreAllMocks();
    global.setInterval = origInterval;
    global.clearInterval = origClear;
  });

  it('calls fetch with params and updates path', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({ json: () => Promise.resolve({ lines: ['A', 'B'] }) })
    );
    const { unmount } = render(<LogViewer path="/a.log" lines={10} />);
    await act(() => Promise.resolve());
    expect(global.fetch).toHaveBeenCalledWith('/logs?path=%2Fa.log&lines=10');
    fireEvent.change(screen.getByDisplayValue('/a.log'), {
      target: { value: '/b.log' },
    });
    await act(() => Promise.resolve());
    expect(global.fetch).toHaveBeenLastCalledWith(
      '/logs?path=%2Fb.log&lines=10'
    );
    unmount();
  });

  it('polls periodically', async () => {
    let count = 0;
    global.fetch = vi.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ lines: [`L${++count}`] }),
      })
    );
    const { unmount } = render(<LogViewer />);
    await act(() => Promise.resolve());
    expect(global.fetch).toHaveBeenCalledTimes(2);
    intervalFn();
    await act(() => Promise.resolve());
    expect(global.fetch).toHaveBeenCalledTimes(3);
    unmount();
  });
  it('filters lines with regex', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({ json: () => Promise.resolve({ lines: ['OK', 'ERR'] }) })
    );
    render(<LogViewer />);
    await act(() => Promise.resolve());
    fireEvent.change(screen.getByPlaceholderText('Filter regex'), {
      target: { value: 'ERR' },
    });
    await act(() => Promise.resolve());
    expect(screen.getByText('ERR')).toBeInTheDocument();
    expect(screen.queryByText('OK')).toBeNull();
  });
});
