import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect } from 'vitest';
import AnomalyDetection from '../src/components/AnomalyDetection.jsx';

describe('AnomalyDetection', () => {
  it('shows anomalies from metrics', () => {
    render(<AnomalyDetection metrics={{ baseline: 'normal', anomalies: ['cpu'] }} />);
    expect(screen.getByText('Baseline: normal')).toBeInTheDocument();
    expect(screen.getByText('cpu')).toBeInTheDocument();
  });
});
