import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import ConsoleView from '../src/components/ConsoleView.jsx';

describe('ConsoleView log viewer', () => {
  let origFetch;

  beforeEach(() => {
    origFetch = global.fetch;
    global.fetch = vi.fn((url) =>
      Promise.resolve({ json: () => Promise.resolve({ lines: ['log'] }) })
    );
  });

  afterEach(() => {
    global.fetch = origFetch;
  });

  it('loads logs on mount', async () => {
    render(<ConsoleView />);
    expect(await screen.findByText('log')).toBeInTheDocument();
  });
});
