import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import IncidentResponse from '../src/components/IncidentResponse.jsx';

describe('IncidentResponse', () => {
  let origFetch;
  beforeEach(() => {
    origFetch = global.fetch;
  });
  afterEach(() => {
    global.fetch = origFetch;
  });

  it('renders incident response metrics', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        json: () =>
          Promise.resolve({
            correlations: [1],
            classifications: [1, 2],
            workflows: ['wf'],
            forensics: [1, 2, 3],
          }),
      })
    );
    render(<IncidentResponse />);
    expect(await screen.findByText('Correlations: 1')).toBeInTheDocument();
    expect(screen.getByText('Classifications: 2')).toBeInTheDocument();
    expect(screen.getByText('Workflows: 1')).toBeInTheDocument();
    expect(screen.getByText('Forensic Items: 3')).toBeInTheDocument();
  });
});
