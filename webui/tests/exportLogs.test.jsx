import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import LogViewer from '../src/components/LogViewer.jsx';

describe('LogViewer', () => {
  let origFetch;
  beforeEach(() => {
    origFetch = global.fetch;
    global.fetch = vi.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ lines: ['line1', 'line2'] }),
      })
    );
  });
  afterEach(() => {
    global.fetch = origFetch;
  });

  it('loads logs for given path and lines', async () => {
    render(<LogViewer path="/tmp/test.log" lines={10} />);
    expect(global.fetch).toHaveBeenCalledWith(
      '/logs?path=%2Ftmp%2Ftest.log&lines=10'
    );
    const pre = await screen.findByText((content, el) => el.tagName === 'PRE');
    expect(pre.textContent).toBe('line1\nline2');
  });
});
