import { describe, it, expect, vi } from 'vitest';
import * as os from '../src/orientationSensors.js';

describe('orientation sensors pkg', () => {
  it('orientation to angle basic', () => {
    expect(os.orientationToAngle('normal')).toBe(0);
    expect(os.orientationToAngle('left-up')).toBe(270);
    expect(os.orientationToAngle('unknown')).toBeUndefined();
  });

  it('orientation to angle with custom map', () => {
    expect(os.orientationToAngle('flip', { flip: 45 })).toBe(45);
  });

  it('update map and reload', () => {
    os.updateOrientationMap({ flip: 45 });
    try {
      expect(os.orientationToAngle('flip')).toBe(45);
    } finally {
      os.resetOrientationMap();
    }
  });

  it('missing dbus', () => {
    const orig = os.dbus;
    os.dbus = null;
    try {
      expect(os.getOrientationDbus()).toBeNull();
    } finally {
      os.dbus = orig;
    }
  });

  it('dbus success', () => {
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

  it('read mpu6050 missing', () => {
    const orig = os.mpu6050;
    os.mpu6050 = null;
    try {
      expect(os.readMpu6050()).toBeNull();
    } finally {
      os.mpu6050 = orig;
    }
  });

  it('read mpu6050 success', () => {
    class DummySensor {
      constructor(addr) {
        this.address = addr;
      }
      get_accel_data() { return { x: 1 }; }
      get_gyro_data() { return { y: 2 }; }
    }
    const orig = os.mpu6050;
    os.mpu6050 = DummySensor;
    try {
      expect(os.readMpu6050()).toEqual({ accelerometer: { x: 1 }, gyroscope: { y: 2 } });
    } finally {
      os.mpu6050 = orig;
    }
  });
});
