import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import ExportCenter from '../src/components/ExportCenter.jsx';

describe('ExportCenter', () => {
  let origFetch;
  beforeEach(() => {
    origFetch = global.fetch;
  });
  afterEach(() => {
    global.fetch = origFetch;
  });

  it('adds download link after export', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({ blob: () => Promise.resolve(new Blob(['x'])) })
    );
    render(<ExportCenter />);
    fireEvent.click(screen.getByText('Start Export'));
    expect(await screen.findByText('Complete')).toBeInTheDocument();
    expect(screen.getByText('Download')).toBeInTheDocument();
  });
});
