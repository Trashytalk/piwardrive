import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import ThreatIntelligence from '../src/components/ThreatIntelligence.jsx';

describe('ThreatIntelligence', () => {
  let origFetch;
  beforeEach(() => {
    origFetch = global.fetch;
  });
  afterEach(() => {
    global.fetch = origFetch;
  });

  it('displays threat intelligence data', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        json: () =>
          Promise.resolve({
            patterns: ['p'],
            actors: ['a'],
            incidents: [1],
            vulnerabilities: ['v'],
            network_score: 80,
            encryption_strength: 90,
            threat_level: 70,
          }),
      })
    );
    render(<ThreatIntelligence />);
    expect(await screen.findByText('Attack Patterns: 1')).toBeInTheDocument();
    expect(screen.getByText('Threat Actors: 1')).toBeInTheDocument();
    expect(screen.getByText('Incidents: 1')).toBeInTheDocument();
    expect(screen.getByText('Security Score: 70')).toBeInTheDocument();
  });
});
