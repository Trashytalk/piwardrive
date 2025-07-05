import { render, screen, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import LiveMonitoring from '../src/components/LiveMonitoring.jsx';
import LiveMetrics from '../src/components/LiveMetrics.jsx';
import ScanningStatus from '../src/components/ScanningStatus.jsx';

let socket;

function mockSocket() {
  socket = {
    send: vi.fn(),
    close: vi.fn(),
    readyState: WebSocket.OPEN
  };
  setTimeout(() => socket.onopen && socket.onopen(), 0);
  return socket;
}

describe('live components', () => {
  beforeEach(() => {
    global.WebSocket = vi.fn(() => mockSocket());
    HTMLCanvasElement.prototype.getContext = vi.fn();
  });

  it('updates live monitoring feed', async () => {
    render(<LiveMonitoring />);
    act(() => {
      socket.onmessage({ data: JSON.stringify({ detection: { text: 'd1' }, stats: { total: 1 } }) });
    });
    expect(await screen.findByText('d1')).toBeInTheDocument();
    expect(screen.getByText('Detections: 1')).toBeInTheDocument();
  });

  it('shows metrics alerts', async () => {
    render(<LiveMetrics />);
    act(() => {
      socket.onmessage({ data: JSON.stringify({ alert: 'ALERT' }) });
    });
    expect(await screen.findByText('ALERT')).toBeInTheDocument();
  });

  it('updates scanning status', async () => {
    render(<ScanningStatus />);
    act(() => {
      socket.onmessage({ data: JSON.stringify({ progress: 50, device: { name: 's1', health: 'ok' } }) });
    });
    expect(await screen.findByText(/s1/)).toBeInTheDocument();
  });
});
