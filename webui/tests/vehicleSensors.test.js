import { describe, it, expect } from 'vitest';
import * as vs from '../src/vehicleSensors.js';

function setObd(value) {
  Object.defineProperty(vs, 'obd', { value, writable: true });
}

describe('vehicleSensors', () => {
  it('returns null when obd missing', () => {
    setObd(null);
    expect(vs.readRpmObd()).toBeNull();
  });

  it('reads values with dummy obd', () => {
    class DummyVal {
      constructor(v) {
        this.v = v;
      }
      to() {
        return this.v;
      }
    }
    class DummyConn {
      query() {
        return { value: new DummyVal(50) };
      }
    }
    setObd({
      OBD: () => new DummyConn(),
      commands: { ENGINE_LOAD: 'ENGINE_LOAD', RPM: 'RPM' },
    });
    expect(vs.readEngineLoadObd()).toBe(50);
    expect(vs.readRpmObd()).toBe(50);
  });
});
