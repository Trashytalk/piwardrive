import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import BatteryStatus from '../src/components/BatteryStatus.jsx';
import ServiceStatus from '../src/components/ServiceStatus.jsx';
import HandshakeCount from '../src/components/HandshakeCount.jsx';
import SignalStrength from '../src/components/SignalStrength.jsx';
import { describe, it, expect } from 'vitest';

describe('dashboard widgets', () => {
  it('shows battery metrics', () => {
    render(
      <BatteryStatus
        metrics={{ battery_percent: 88.4, battery_plugged: true }}
      />
    );
    expect(screen.getByText('Battery: 88% charging')).toBeInTheDocument();
  });

  it('handles missing battery metrics', () => {
    render(<BatteryStatus />);
    expect(screen.getByText('Battery: N/A')).toBeInTheDocument();
  });

  it('shows service status', () => {
    render(
      <ServiceStatus
        metrics={{ kismet_running: true, bettercap_running: false }}
      />
    );
    expect(screen.getByText('Kismet: ok')).toBeInTheDocument();
    expect(screen.getByText('BetterCAP: down')).toBeInTheDocument();
  });

  it('displays handshake count', () => {
    render(<HandshakeCount metrics={{ handshake_count: 7 }} />);
    expect(screen.getByText('Handshakes: 7')).toBeInTheDocument();
  });

  it('shows RSSI', () => {
    render(<SignalStrength metrics={{ avg_rssi: -42.5 }} />);
    expect(screen.getByText('RSSI: -42.5 dBm')).toBeInTheDocument();
  });
});
