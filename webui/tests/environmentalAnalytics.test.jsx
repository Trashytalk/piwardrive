import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import EnvironmentalAnalytics from '../src/components/EnvironmentalAnalytics.jsx';

vi.mock('react-chartjs-2', () => ({ Line: () => <canvas></canvas> }));

describe('EnvironmentalAnalytics', () => {
  let origFetch;
  beforeEach(() => {
    origFetch = global.fetch;
    global.fetch = vi
      .fn()
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ current_weather: { temperature: 10 } }),
      })
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ list: [{}, {}] }),
      })
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ new_projects: 5 }),
      });
    vi.setSystemTime(new Date('2023-06-15'));
  });
  afterEach(() => {
    global.fetch = origFetch;
  });

  it('shows analytics summary', async () => {
    render(<EnvironmentalAnalytics />);
    expect(
      await screen.findByText('Corr:20.0 Season:Summer Events:2 Growth:5')
    ).toBeInTheDocument();
  });
});
