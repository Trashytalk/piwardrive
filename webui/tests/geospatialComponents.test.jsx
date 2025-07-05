import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { vi, describe, it, beforeEach, afterEach } from 'vitest';
import GeospatialAnalytics from '../src/components/GeospatialAnalytics.jsx';
import RFEnvironmentMap from '../src/components/RFEnvironmentMap.jsx';
import InfrastructurePlanner from '../src/components/InfrastructurePlanner.jsx';

vi.mock('react-leaflet', () => ({
  MapContainer: ({ children }) => <div data-testid="map">{children}</div>,
  TileLayer: () => <div>tile</div>,
  CircleMarker: ({ children }) => <div>{children}</div>,
  Marker: ({ children }) => <div>{children}</div>,
  Popup: ({ children }) => <div>{children}</div>,
  Polygon: ({ children }) => <div>{children}</div>,
}));

describe('geospatial components', () => {
  let origFetch;
  beforeEach(() => {
    origFetch = global.fetch;
  });
  afterEach(() => {
    global.fetch = origFetch;
  });

  it('renders GeospatialAnalytics', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({ json: () => Promise.resolve({}) })
    );
    render(<GeospatialAnalytics />);
    expect(screen.getByTestId('map')).toBeInTheDocument();
    await waitFor(() => expect(global.fetch).toHaveBeenCalled());
  });

  it('renders RFEnvironmentMap', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({ json: () => Promise.resolve({}) })
    );
    render(<RFEnvironmentMap />);
    expect(screen.getByTestId('map')).toBeInTheDocument();
    await waitFor(() => expect(global.fetch).toHaveBeenCalled());
  });

  it('renders InfrastructurePlanner', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({ json: () => Promise.resolve({}) })
    );
    render(<InfrastructurePlanner />);
    expect(screen.getByTestId('map')).toBeInTheDocument();
    await waitFor(() => expect(global.fetch).toHaveBeenCalled());
  });
});
