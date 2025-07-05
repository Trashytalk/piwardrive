import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect } from 'vitest';
import MLDashboard from '../src/components/MLDashboard.jsx';

describe('MLDashboard', () => {
  it('renders metrics from props', () => {
    render(
      <MLDashboard
        metrics={{
          performance: 'ok',
          accuracy: 0.9,
          progress: 50,
          features: [{ name: 'a', importance: 0.5 }],
        }}
      />
    );
    expect(screen.getByText('Performance: ok')).toBeInTheDocument();
    expect(screen.getByText('Accuracy: 0.9')).toBeInTheDocument();
    expect(screen.getByText(/a:/)).toBeInTheDocument();
  });
});
