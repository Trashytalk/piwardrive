import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, vi } from 'vitest';
import GPSStatus from '../src/components/GPSStatus.jsx';

describe('GPSStatus async failure', () => {
  it('shows Unknown/N/A when fetch fails', async () => {
    let origFetch = global.fetch;
    global.fetch = vi.fn(() => Promise.reject('fail'));
    render(<GPSStatus />);
    expect(await screen.findByText('GPS: N/A')).toBeInTheDocument();
    global.fetch = origFetch;
  });
});
