import { reportError } from './exceptionHandler.js';

export const DEFAULT_ORIENTATION_MAP = {
  normal: 0.0,
  'bottom-up': 180.0,
  'right-up': 90.0,
  'left-up': 270.0,
  portrait: 0.0,
  'portrait-upside-down': 180.0,
  'landscape-left': 90.0,
  'landscape-right': 270.0,
  'upside-down': 180.0,
};

let ORIENTATION_MAP = { ...DEFAULT_ORIENTATION_MAP };

export function orientationToAngle(orientation, orientationMap) {
  const map = orientationMap || ORIENTATION_MAP;
  if (!orientation) return undefined;
  return map[orientation.toLowerCase()];
}

export function cloneOrientationMap() {
  return { ...ORIENTATION_MAP };
}

export function resetOrientationMap() {
  ORIENTATION_MAP = { ...DEFAULT_ORIENTATION_MAP };
}

export function updateOrientationMap(
  newMap,
  { clear = false, mapping = null } = {}
) {
  const target = mapping || ORIENTATION_MAP;
  if (clear) {
    for (const k in target) delete target[k];
  }
  for (const [k, v] of Object.entries(newMap)) {
    target[k.toLowerCase()] = v;
  }
  return target;
}

export let dbus = null;
export let mpu6050 = null;

export function getOrientationDbus() {
  if (!dbus) return null;
  try {
    const bus = dbus.SystemBus();
    const proxy = bus.get_object(
      'net.hadess.SensorProxy',
      '/net/hadess/SensorProxy'
    );
    const iface = dbus.Interface(proxy, 'net.hadess.SensorProxy');
    if (!iface.HasAccelerometer()) return null;
    iface.ClaimAccelerometer();
    try {
      return iface.GetAccelerometerOrientation();
    } finally {
      iface.ReleaseAccelerometer();
    }
  } catch (e) {
    reportError(e);
    return null;
  }
}

export function readMpu6050(address = 0x68) {
  if (!mpu6050) return null;
  try {
    const sensor = new mpu6050(address);
    return {
      accelerometer: sensor.get_accel_data(),
      gyroscope: sensor.get_gyro_data(),
    };
  } catch (e) {
    reportError(e);
    return null;
  }
}

export function getHeading(orientationMap) {
  const orient = getOrientationDbus();
  if (orient) {
    return orientationToAngle(orient, orientationMap);
  }
  return null;
}
