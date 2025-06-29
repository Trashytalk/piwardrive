export interface OrientationMap {
  [orientation: string]: number;
}

export const DEFAULT_ORIENTATION_MAP: OrientationMap;

export function orientationToAngle(
  orientation: string | undefined,
  orientationMap?: OrientationMap
): number | undefined;

export function cloneOrientationMap(): OrientationMap;

export function resetOrientationMap(): void;

export interface UpdateOrientationMapOptions {
  clear?: boolean;
  mapping?: OrientationMap | null;
}

export function updateOrientationMap(
  newMap: OrientationMap,
  options?: UpdateOrientationMapOptions
): OrientationMap;

export let dbus: any;
export let mpu6050: any;

export function getOrientationDbus(): string | null;

export interface Mpu6050Reading {
  accelerometer: any;
  gyroscope: any;
}

export function readMpu6050(address?: number): Mpu6050Reading | null;

export function getHeading(orientationMap?: OrientationMap): number | null | undefined;
