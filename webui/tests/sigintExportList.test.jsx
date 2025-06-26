import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { vi, describe, it, beforeEach, afterEach } from 'vitest';
import SigintExportList from '../src/components/SigintExportList.jsx';

describe('SigintExportList', () => {
  let origFetch;
  beforeEach(() => { origFetch = global.fetch; });
  afterEach(() => { global.fetch = origFetch; });

  it('shows record count', async () => {
    global.fetch = vi.fn(() => Promise.resolve({ json: () => Promise.resolve([{a:1},{a:2}]) }));
    render(<SigintExportList type="aps" />);
    expect(await screen.findByTestId('count')).toHaveTextContent('count 2');
  });
});
