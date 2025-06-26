import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import DBStats from '../src/components/DBStats.jsx';

describe('DBStats', () => {
  let origFetch;
  beforeEach(() => { origFetch = global.fetch; });
  afterEach(() => { global.fetch = origFetch; });

  it('displays database stats', async () => {
    global.fetch = vi.fn(() => Promise.resolve({ json: () => Promise.resolve({ size_kb: 2.0, tables: { ap_cache: 2 } }) }));
    render(<DBStats />);
    expect(await screen.findByText('DB: 2.0KB ap_cache:2')).toBeInTheDocument();
  });
});
