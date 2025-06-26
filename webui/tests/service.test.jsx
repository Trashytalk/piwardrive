import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, waitFor } from '@testing-library/react';
vi.mock('chart.js', () => ({
  Chart: { register: vi.fn() },
  CategoryScale: {},
  LinearScale: {},
  PointElement: {},
  LineElement: {}
}));
vi.mock('react-chartjs-2', () => ({ Line: () => <div /> }));
import StatsDashboard from '../src/components/StatsDashboard.jsx';

let origFetch;

describe('StatsDashboard', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    origFetch = global.fetch;
    global.fetch = vi.fn(url => {
      const map = {
        '/cpu': { percent: 10 },
        '/ram': { percent: 20 },
        '/storage': { percent: 30 }
      };
      return Promise.resolve({ json: () => Promise.resolve(map[url]) });
    });
  });

  afterEach(() => {
    vi.useRealTimers();
    global.fetch = origFetch;
  });

  it.skip('polls metrics and updates charts', async () => {
    render(<StatsDashboard />);
    vi.advanceTimersByTime(2100);
    await waitFor(() => expect(global.fetch).toHaveBeenCalled());
  });
});
