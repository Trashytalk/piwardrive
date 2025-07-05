import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom';
import { computeHealthStats } from '../src/analysis.js';
import CPUTempGraph from '../src/components/CPUTempGraph.jsx';

vi.mock('react-chartjs-2', () => ({
  Line: vi.fn(() => <div>chart</div>),
}));
import { Line } from 'react-chartjs-2';

describe('computeHealthStats', () => {
  it('computes averages', () => {
    const records = [
      {
        cpu_temp: 40.0,
        cpu_percent: 10.0,
        memory_percent: 50.0,
        disk_percent: 20.0,
      },
      {
        cpu_temp: 50.0,
        cpu_percent: 20.0,
        memory_percent: 40.0,
        disk_percent: 30.0,
      },
    ];
    const stats = computeHealthStats(records);
    expect(stats.temp_avg).toBeCloseTo(45.0, 1);
    expect(stats.cpu_avg).toBe(15.0);
  });
});

describe('CPUTempGraph', () => {
  it('renders chart data', () => {
    const { rerender } = render(<CPUTempGraph metrics={{ cpu_temp: 40 }} />);
    expect(Line).toHaveBeenCalled();
    const firstCall = Line.mock.calls[0][0];
    expect(firstCall.data.datasets[0].data).toEqual([40]);
    Line.mockClear();
    rerender(<CPUTempGraph metrics={{ cpu_temp: 50 }} />);
    expect(Line).toHaveBeenCalled();
    const secondCall = Line.mock.calls[0][0];
    expect(secondCall.data.datasets[0].data).toEqual([40, 50]);
  });
});
