import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import EventDetector from '../src/components/EventDetector.jsx';

describe('EventDetector', () => {
  let origFetch;
  beforeEach(() => {
    origFetch = global.fetch;
    global.fetch = vi
      .fn()
      .mockResolvedValueOnce({
        json: () =>
          Promise.resolve({
            list: [
              { crowd: 70, special: true, type: 'concert' },
              { crowd: 5, type: 'emergency' },
            ],
          }),
      })
      .mockResolvedValueOnce({
        json: () =>
          Promise.resolve({ response: { holidays: [{ name: 'Holiday' }] } }),
      });
  });
  afterEach(() => {
    global.fetch = origFetch;
  });

  it('detects events', async () => {
    render(<EventDetector />);
    expect(
      await screen.findByText('Crowd:1 Emergency:1 Special:2')
    ).toBeInTheDocument();
  });
});
