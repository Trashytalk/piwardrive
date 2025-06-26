import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { vi, describe, it, beforeEach, afterEach } from 'vitest';
import SyncButton from '../src/components/SyncButton.jsx';

describe('SyncButton', () => {
  let origFetch;
  beforeEach(() => { origFetch = global.fetch; });
  afterEach(() => { global.fetch = origFetch; });

  it('shows success', async () => {
    global.fetch = vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({ uploaded: 2 }) }));
    render(<SyncButton limit={2} />);
    fireEvent.click(screen.getByText('Sync'));
    expect(await screen.findByTestId('result')).toHaveTextContent('uploaded 2');
  });

  it('shows failure', async () => {
    global.fetch = vi.fn(() => Promise.resolve({ ok: false }));
    render(<SyncButton />);
    fireEvent.click(screen.getByText('Sync'));
    expect(await screen.findByTestId('result')).toHaveTextContent('failed');
  });
});
