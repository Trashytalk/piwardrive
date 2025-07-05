/* global process */
const DEFAULT_EXPORT_DIR = '/exports';
export const EXPORT_DIR = process.env.EXPORT_DIR || DEFAULT_EXPORT_DIR;
