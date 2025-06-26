import { describe, it, expect, vi } from 'vitest';
import * as os from '../src/orientationSensors.js';

describe('orientation helpers', () => {
  it('maps orientation to angle', () => {
    expect(os.orientationToAngle('normal')).toBe(0);
    expect(os.orientationToAngle('left-up')).toBe(270);
    expect(os.orientationToAngle('unknown')).toBeUndefined();
  });

  it('uses custom map', () => {
    const map = { flip: 45 };
    expect(os.orientationToAngle('flip', map)).toBe(45);
  });

  it('updates global map', () => {
    os.updateOrientationMap({ flip: 45 });
    try {
      expect(os.orientationToAngle('flip')).toBe(45);
    } finally {
      os.resetOrientationMap();
    }
  });

  it('updates separate map copy', () => {
    const local = os.cloneOrientationMap();
    os.updateOrientationMap({ flip: 45 }, { mapping: local });
    expect(os.orientationToAngle('flip', local)).toBe(45);
    expect(os.orientationToAngle('flip')).toBeUndefined();
  });

  it('handles missing dbus gracefully', () => {
    const orig = os.dbus;
    os.dbus = null;
    try {
      expect(os.getOrientationDbus()).toBeNull();
    } finally {
      os.dbus = orig;
    }
  });

  it('reads orientation via dbus', () => {
    const dummyIface = {
      HasAccelerometer: () => true,
      ClaimAccelerometer: vi.fn(),
      ReleaseAccelerometer: vi.fn(),
      GetAccelerometerOrientation: () => 'right-up',
    };
    const dummyBus = { get_object: () => ({}) };
    const iface = () => dummyIface;
    const dummyDbus = { SystemBus: () => dummyBus, Interface: iface };
    const orig = os.dbus;
    os.dbus = dummyDbus;
    try {
      expect(os.getOrientationDbus()).toBe('right-up');
    } finally {
      os.dbus = orig;
    }
  });

  it('computes heading from orientation', () => {
    const origGet = os.getOrientationDbus;
    os.getOrientationDbus = () => 'right-up';
    const origMap = os.orientationToAngle;
    os.orientationToAngle = () => 90;
    try {
      expect(os.getHeading()).toBe(90);
    } finally {
      os.getOrientationDbus = origGet;
      os.orientationToAngle = origMap;
    }
  });

  it('returns null heading when no orientation', () => {
    const orig = os.getOrientationDbus;
    os.getOrientationDbus = () => null;
    try {
      expect(os.getHeading()).toBeNull();
    } finally {
      os.getOrientationDbus = orig;
    }
  });
});
