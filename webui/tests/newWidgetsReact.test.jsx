import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import GPSStatus from '../src/components/GPSStatus.jsx';
import ServiceStatus from '../src/components/ServiceStatus.jsx';
import HandshakeCount from '../src/components/HandshakeCount.jsx';
import StorageUsage from '../src/components/StorageUsage.jsx';
import SignalStrength from '../src/components/SignalStrength.jsx';

describe('new widget equivalents', () => {
  it('gps status with metrics', () => {
    render(<GPSStatus metrics={{ gps_fix: '3D' }} />);
    expect(screen.getByText('GPS: 3D')).toBeInTheDocument();
  });

  it('service status displays ok/down', () => {
    render(
      <ServiceStatus
        metrics={{ kismet_running: true, bettercap_running: false }}
      />
    );
    expect(screen.getByText('Kismet: ok')).toBeInTheDocument();
    expect(screen.getByText('BetterCAP: down')).toBeInTheDocument();
  });

  it('handshake count shows number', () => {
    render(<HandshakeCount metrics={{ handshake_count: 7 }} />);
    expect(screen.getByText('Handshakes: 7')).toBeInTheDocument();
  });

  it('storage usage fetches percent', async () => {
    const origFetch = global.fetch;
    global.fetch = vi.fn(() =>
      Promise.resolve({ json: () => Promise.resolve({ percent: 55 }) })
    );
    render(<StorageUsage />);
    await waitFor(() =>
      expect(screen.getByText('SSD: 55%')).toBeInTheDocument()
    );
    global.fetch = origFetch;
  });

  it('signal strength displays rssi', () => {
    render(<SignalStrength metrics={{ avg_rssi: -42 }} />);
    expect(screen.getByText('RSSI: -42.0 dBm')).toBeInTheDocument();
  });
});
