import * as net from 'net';

const DEFAULT_PATH = '/var/run/gpsd.sock';

export async function getFix(timeoutMs = 1000, socketPath = DEFAULT_PATH) {
  return new Promise((resolve) => {
    const client = net.createConnection({ path: socketPath });
    client.on('connect', () => {
      client.write('?WATCH={"enable":true,"json":true};\n');
    });

    let buffer = '';
    const finish = (data) => {
      cleanup();
      resolve(data);
    };

    const timer = setTimeout(() => finish(null), timeoutMs);

    function cleanup() {
      clearTimeout(timer);
      client.removeAllListeners();
      client.destroy();
    }

    client.on('data', (chunk) => {
      buffer += chunk.toString();
      let idx;
      while ((idx = buffer.indexOf('\n')) >= 0) {
        const line = buffer.slice(0, idx).trim();
        buffer = buffer.slice(idx + 1);
        if (!line) continue;
        let obj;
        try {
          obj = JSON.parse(line);
        } catch {
          continue;
        }
        if (obj.class === 'TPV') {
          finish(obj);
          return;
        }
      }
    });

    client.on('error', () => finish(null));
  });
}
