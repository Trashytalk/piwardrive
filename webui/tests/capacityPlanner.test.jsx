import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import CapacityPlanner from '../src/components/CapacityPlanner.jsx';

describe('CapacityPlanner', () => {
  let origFetch;
  beforeEach(() => {
    origFetch = global.fetch;
  });
  afterEach(() => {
    global.fetch = origFetch;
  });

  it('fetches capacity data', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ forecast: [1], confidence: [0.1] }),
      })
    );
    render(<CapacityPlanner />);
    expect(await screen.findByText(/Usage Forecast/)).toBeInTheDocument();
  });
});
