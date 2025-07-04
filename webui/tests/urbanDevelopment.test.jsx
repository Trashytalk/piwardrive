import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import UrbanDevelopment from '../src/components/UrbanDevelopment.jsx';

describe('UrbanDevelopment', () => {
  let origFetch;
  beforeEach(() => {
    origFetch = global.fetch;
    global.fetch = vi.fn(() =>
      Promise.resolve({
        json: () =>
          Promise.resolve({
            infrastructure_growth: 2,
            development_pattern: 'cluster',
            gentrification_index: 0.3,
            smart_city_score: 0.8,
          }),
      })
    );
  });
  afterEach(() => {
    global.fetch = origFetch;
  });

  it('shows development metrics', async () => {
    render(<UrbanDevelopment />);
    expect(
      await screen.findByText(
        'Growth:2 Pattern:cluster Gentrification:0.3 Smart:0.8'
      )
    ).toBeInTheDocument();
  });
});
