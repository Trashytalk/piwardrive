export let obd = null;

export function readSpeedObd(port = null) {
  if (!obd) return null;
  try {
    const conn = new obd.OBD(port);
    const rsp = conn.query(obd.commands.SPEED);
    return rsp && rsp.value != null ? Number(rsp.value.to('km/h')) : null;
  } catch (e) {
    console.error('OBD speed read failed:', e);
    return null;
  }
}

export function readRpmObd(port = null) {
  if (!obd) return null;
  try {
    const conn = new obd.OBD(port);
    const rsp = conn.query(obd.commands.RPM);
    return rsp && rsp.value != null ? Number(rsp.value.to('rpm')) : null;
  } catch (e) {
    console.error('OBD RPM read failed:', e);
    return null;
  }
}

export function readEngineLoadObd(port = null) {
  if (!obd) return null;
  try {
    const conn = new obd.OBD(port);
    const rsp = conn.query(obd.commands.ENGINE_LOAD);
    return rsp && rsp.value != null ? Number(rsp.value.to('percent')) : null;
  } catch (e) {
    console.error('OBD engine load read failed:', e);
    return null;
  }
}
