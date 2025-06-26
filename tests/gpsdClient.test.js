const test = require('node:test');
const assert = require('node:assert/strict');
const Module = require('module');
const path = require('path');

function reloadWithDummy({ connectOk = true, packet = null, raiseOnGet = false, getCurrent } = {}) {
  const dummy = {
    connect: () => {
      if (!connectOk) throw new Error('fail');
    },
    getCurrent: getCurrent || (() => {
      if (raiseOnGet) throw new Error('boom');
      return packet;
    }),
  };

  const original = Module._load;
  Module._load = (request, parent, isMain) => {
    if (request === 'gpsd') return dummy;
    return original(request, parent, isMain);
  };

  delete require.cache[require.resolve('../scripts/gpsdClient.js')];
  const mod = require('../scripts/gpsdClient.js');
  Module._load = original;
  return mod;
}

test('getPosition returns null on failure', () => {
  const mod = reloadWithDummy({ connectOk: false });
  assert.equal(mod.client.getPosition(), null);
});

test('reconnect after error', () => {
  const pkt = { mode: 3, lat: 1.0, lon: 2.0, error: { x: 1.0, y: 1.0 } };
  let first = true;
  function getCurrent() {
    if (first) { first = false; throw new Error('fail'); }
    return pkt;
  }
  const mod = reloadWithDummy({ getCurrent });
  assert.equal(mod.client.getPosition(), null);
  assert.deepStrictEqual(mod.client.getPosition(), [1.0, 2.0]);
});

test('env overrides', () => {
  process.env.PW_GPSD_HOST = '1.2.3.4';
  process.env.PW_GPSD_PORT = '1234';
  const mod = reloadWithDummy();
  delete process.env.PW_GPSD_HOST;
  delete process.env.PW_GPSD_PORT;
  assert.equal(mod.client.host, '1.2.3.4');
  assert.equal(mod.client.port, 1234);
});
