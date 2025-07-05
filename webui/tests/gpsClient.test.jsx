import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import GPSStatus from '../src/components/GPSStatus.jsx';

describe('GPSStatus', () => {
  it('uses metrics when provided', () => {
    render(<GPSStatus metrics={{ gps_fix: '3D' }} />);
    expect(screen.getByText('GPS: 3D')).toBeInTheDocument();
  });

  it('fetches fix quality', async () => {
    let origFetch = global.fetch;
    global.fetch = vi.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ fix: '2D' }),
      })
    );
    render(<GPSStatus />);
    expect(await screen.findByText('GPS: 2D')).toBeInTheDocument();
    global.fetch = origFetch;
  });

  it('handles fetch failure', async () => {
    let origFetch = global.fetch;
    global.fetch = vi.fn(() => Promise.reject('fail'));
    render(<GPSStatus />);
    expect(await screen.findByText('GPS: N/A')).toBeInTheDocument();
    global.fetch = origFetch;
  });
});
