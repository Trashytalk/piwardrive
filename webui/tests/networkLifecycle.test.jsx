import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import NetworkLifecycle from '../src/components/NetworkLifecycle.jsx';

describe('NetworkLifecycle', () => {
  let origFetch;
  beforeEach(() => {
    origFetch = global.fetch;
  });
  afterEach(() => {
    global.fetch = origFetch;
  });

  it('fetches lifecycle data', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ forecast: [1], confidence: [0.1] }),
      })
    );
    render(<NetworkLifecycle />);
    expect(await screen.findByText(/Upgrade Prediction/)).toBeInTheDocument();
  });
});
