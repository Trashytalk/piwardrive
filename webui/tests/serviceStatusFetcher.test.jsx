import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { vi, describe, it, beforeEach, afterEach } from 'vitest';
import ServiceStatusFetcher from '../src/components/ServiceStatusFetcher.jsx';

describe('ServiceStatusFetcher', () => {
  let origFetch;
  beforeEach(() => { origFetch = global.fetch; });
  afterEach(() => { global.fetch = origFetch; });

  it('fetches statuses', async () => {
    global.fetch = vi.fn(url => Promise.resolve({ json: () => Promise.resolve({ active: url.includes('kismet') }) }));
    render(<ServiceStatusFetcher services={['kismet', 'gpsd']} />);
    expect(await screen.findByTestId('kismet')).toHaveTextContent('kismet: active');
    expect(await screen.findByTestId('gpsd')).toHaveTextContent('gpsd: inactive');
  });
});
