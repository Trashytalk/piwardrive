import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import Orientation from '../src/components/Orientation.jsx';
import VehicleSpeed from '../src/components/VehicleSpeed.jsx';
import LoRaScan, { LoRaScanStatic } from '../src/components/LoRaScan.jsx';

describe('extra widgets', () => {
  it('shows orientation text', () => {
    render(<Orientation data={{ orientation: 'right-up', angle: 90 }} />);
    expect(screen.getByText('Orientation: right-up (90\u00B0)')).toBeInTheDocument();
  });

  it('shows vehicle speed', () => {
    render(<VehicleSpeed metrics={{ vehicle_speed: 42.5 }} />);
    expect(screen.getByText('Vehicle Speed: 42.5 km/h')).toBeInTheDocument();
  });

  it('renders LoRa count from metrics', () => {
    render(<LoRaScanStatic metrics={{ lora_devices: 3 }} />);
    expect(screen.getByText('LoRa: 3')).toBeInTheDocument();
  });

  it('fetches LoRa scan results', async () => {
    let origFetch = global.fetch;
    global.fetch = vi.fn(() => Promise.resolve({
      json: () => Promise.resolve({ output: 'a\nb\nc' })
    }));
    render(<LoRaScan />);
    expect(await screen.findByText('LoRa Devices: 3')).toBeInTheDocument();
    global.fetch = origFetch;
  });
});
