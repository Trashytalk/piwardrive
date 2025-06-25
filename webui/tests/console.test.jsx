import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, vi } from 'vitest';
import ConsoleView from '../src/components/ConsoleView.jsx';

vi.stubGlobal('fetch', vi.fn());

const cfgResp = { json: () => Promise.resolve({ log_paths: ['/a', '/b'] }) };
const logResp = { json: () => Promise.resolve({ lines: ['hello'] }) };

fetch.mockResolvedValueOnce(cfgResp).mockResolvedValueOnce(logResp);


describe('console view', () => {
  it('shows logs and path selector', async () => {
    render(<ConsoleView />);
    await waitFor(() => {
      expect(screen.getByText('hello')).toBeInTheDocument();
    });
    expect(screen.getByRole('combobox')).toBeInTheDocument();
  });
});
