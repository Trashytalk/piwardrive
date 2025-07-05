import { describe, it, expect, vi } from 'vitest';
import { Container } from '../src/di.ts';

describe('Container', () => {
  it('registers instance and resolves', () => {
    const c = new Container();
    const obj = {};
    c.registerInstance('svc', obj);
    expect(c.has('svc')).toBe(true);
    expect(c.resolve('svc')).toBe(obj);
  });

  it('registers factory and returns single instance', () => {
    const c = new Container();
    const factory = vi.fn(() => ({}));
    c.registerFactory('svc', factory);
    const first = c.resolve('svc');
    const second = c.resolve('svc');
    expect(first).toBe(second);
    expect(factory).toHaveBeenCalledTimes(1);
  });

  it('throws for missing key', () => {
    const c = new Container();
    expect(() => c.resolve('missing')).toThrow();
  });

  it('resolves single instance when called concurrently', async () => {
    const c = new Container();
    const factory = vi.fn(() => ({}));
    c.registerFactory('svc', factory);
    const results = await Promise.all(
      Array.from({ length: 10 }, () =>
        Promise.resolve().then(() => c.resolve('svc'))
      )
    );
    expect(factory).toHaveBeenCalledTimes(1);
    results.forEach((r) => expect(r).toBe(results[0]));
  });
});
