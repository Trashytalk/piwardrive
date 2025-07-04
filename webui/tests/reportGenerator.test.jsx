import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import ReportGenerator from '../src/components/ReportGenerator.jsx';

describe('ReportGenerator', () => {
  let origFetch;
  beforeEach(() => {
    origFetch = global.fetch;
  });
  afterEach(() => {
    global.fetch = origFetch;
  });

  it('shows preview after generation', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({ text: () => Promise.resolve('rpt') })
    );
    render(<ReportGenerator />);
    fireEvent.click(screen.getByText('Generate'));
    expect(await screen.findByText('rpt')).toBeInTheDocument();
  });
});
