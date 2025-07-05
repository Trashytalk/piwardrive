import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, vi } from 'vitest';
import DatabaseConfig from '../src/components/DatabaseConfig.jsx';

describe('DatabaseConfig', () => {
  it('calls onChange for inputs', () => {
    const cfg = {
      db_cache_size: 128,
      retention_days: 7,
      backup_enabled: false,
      migration_running: false,
    };
    const onChange = vi.fn();
    render(<DatabaseConfig config={cfg} onChange={onChange} />);
    fireEvent.change(screen.getByLabelText('Cache Size (MB)'), {
      target: { value: '256' },
    });
    expect(onChange).toHaveBeenCalledWith('db_cache_size', 256);
    fireEvent.click(screen.getByLabelText('Backup Enabled'));
    expect(onChange).toHaveBeenLastCalledWith('backup_enabled', true);
  });
});
