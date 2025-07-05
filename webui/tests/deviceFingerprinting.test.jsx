import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect } from 'vitest';
import DeviceFingerprinting from '../src/components/DeviceFingerprinting.jsx';

describe('DeviceFingerprinting', () => {
  it('lists device info', () => {
    render(
      <DeviceFingerprinting
        metrics={{
          devices: [{ device_type: 'phone', vendor: 'Apple', confidence: 0.8 }],
        }}
      />
    );
    expect(screen.getByText(/phone/)).toBeInTheDocument();
    expect(screen.getByText(/Apple/)).toBeInTheDocument();
  });
});
