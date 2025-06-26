import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import HealthAnalysis from '../src/components/HealthAnalysis.jsx';
vi.mock('react-chartjs-2', () => ({ Line: () => <canvas></canvas> }));

describe('HealthAnalysis', () => {
  let origFetch;
  beforeEach(() => {
    origFetch = global.fetch;
    global.fetch = vi.fn(() => Promise.resolve({
      json: () => Promise.resolve([
        { system: { cpu_temp: 40, mem_percent: 20, disk_percent: 10 } },
        { system: { cpu_temp: 60, mem_percent: 40, disk_percent: 20 } }
      ])
    }));
  });
  afterEach(() => {
    global.fetch = origFetch;
  });

  it('shows averaged health stats', async () => {
    render(<HealthAnalysis />);
    expect(await screen.findByText('Temp:50.0°C Mem:30% Disk:15%')).toBeInTheDocument();
  });
});
