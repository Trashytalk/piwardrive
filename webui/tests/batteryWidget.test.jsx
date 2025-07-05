import { render } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect } from 'vitest';
import BatteryStatus from '../src/components/BatteryStatus.jsx';

describe('BatteryStatus widget', () => {
  it('updates when metrics change', () => {
    const { rerender, getByText } = render(
      <BatteryStatus
        metrics={{ battery_percent: 50, battery_plugged: false }}
      />
    );
    expect(getByText('Battery: 50% discharging')).toBeInTheDocument();
    rerender(
      <BatteryStatus metrics={{ battery_percent: 75, battery_plugged: true }} />
    );
    expect(getByText('Battery: 75% charging')).toBeInTheDocument();
  });
});
