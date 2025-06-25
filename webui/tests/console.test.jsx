import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import ConsoleView from '../src/components/ConsoleView.jsx';

describe('ConsoleView command runner', () => {
  let origFetch;

  beforeEach(() => {
    origFetch = global.fetch;
    global.fetch = vi.fn((url) => {
      if (url.startsWith('/logs')) {
        return Promise.resolve({ json: () => Promise.resolve({ lines: ['log'] }) });
      }
      return Promise.resolve({ json: () => Promise.resolve({ output: 'pong' }) });
    });
  });

  afterEach(() => {
    global.fetch = origFetch;
  });

  it('sends command and shows output', async () => {
    render(<ConsoleView />);
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'ping' } });
    fireEvent.click(screen.getByText('Run'));
    expect(await screen.findByText('Command Output')).toBeInTheDocument();
    expect(screen.getByText('pong')).toBeInTheDocument();
  });
});
