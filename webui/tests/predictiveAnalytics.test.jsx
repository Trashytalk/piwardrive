import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import PredictiveAnalytics from '../src/components/PredictiveAnalytics.jsx';

describe('PredictiveAnalytics', () => {
  let origFetch;
  beforeEach(() => {
    origFetch = global.fetch;
  });
  afterEach(() => {
    global.fetch = origFetch;
  });

  it('shows forecast data', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        json: () =>
          Promise.resolve({
            lifecycle: { forecast: [1], confidence: [0.1] },
            capacity: { forecast: [2], confidence: [0.2] },
            failure: { forecast: [0.3], confidence: [0.05] },
            expansion: ['ap1'],
          }),
      })
    );
    render(<PredictiveAnalytics />);
    expect(await screen.findByText(/Lifecycle Prediction/)).toBeInTheDocument();
  });
});
