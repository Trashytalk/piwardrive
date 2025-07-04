import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import ReportDashboard from '../src/components/ReportDashboard.jsx';

describe('ReportDashboard', () => {
  let origFetch;
  beforeEach(() => {
    origFetch = global.fetch;
  });
  afterEach(() => {
    global.fetch = origFetch;
  });

  it('filters report list', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve([{ id: 1, name: 'A', url: '/a' }]),
      })
    );
    render(<ReportDashboard />);
    expect(await screen.findByText('A')).toBeInTheDocument();
    fireEvent.change(screen.getByPlaceholderText('Search'), {
      target: { value: 'x' },
    });
    expect(screen.queryByText('A')).toBeNull();
  });
});
