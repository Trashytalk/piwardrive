import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect } from 'vitest';
import IoTAnalytics from '../src/components/IoTAnalytics.jsx';
import SmartCityDashboard from '../src/components/SmartCityDashboard.jsx';
import CriticalInfrastructure from '../src/components/CriticalInfrastructure.jsx';

describe('iot components', () => {
  it('renders IoT analytics metrics', () => {
    render(
      <IoTAnalytics
        metrics={{
          device_classification: 'cams',
          infrastructure_mapping: 'map',
          critical_infrastructure: 'power',
          privacy_risk: 'low',
        }}
      />
    );
    expect(screen.getByText('Classification: cams')).toBeInTheDocument();
    expect(screen.getByText('Infrastructure Map: map')).toBeInTheDocument();
  });

  it('renders smart city metrics', () => {
    render(
      <SmartCityDashboard
        metrics={{
          deployment_map: 'city',
          infrastructure_growth: 'fast',
          service_availability: '99%',
          digital_quality: 'good',
        }}
      />
    );
    expect(screen.getByText('Deployment Map: city')).toBeInTheDocument();
    expect(screen.getByText('Digital Quality: good')).toBeInTheDocument();
  });

  it('renders critical infrastructure metrics', () => {
    render(
      <CriticalInfrastructure
        metrics={{
          industrial_networks: 'nets',
          medical_devices: 'med',
          utility_networks: 'util',
          public_safety_comms: 'ps',
        }}
      />
    );
    expect(screen.getByText('Industrial Networks: nets')).toBeInTheDocument();
    expect(screen.getByText('Public Safety Comms: ps')).toBeInTheDocument();
  });
});
