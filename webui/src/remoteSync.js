// Remote sync utilities similar to Python remote_sync module

export async function syncDatabaseToServer(dbPath, url, { timeout = 30, retries = 3, rowRange = null } = {}) {
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const controller = new AbortController();
      const id = setTimeout(() => controller.abort(), timeout * 1000);
      const resp = await fetch(url, {
        method: 'POST',
        body: rowRange ? JSON.stringify({ dbPath, rowRange }) : dbPath,
        signal: controller.signal,
      });
      clearTimeout(id);
      if (!resp.ok) throw new Error('upload failed');
      return true;
    } catch (e) {
      if (attempt === retries) throw e;
      await new Promise(r => setTimeout(r, 1000));
    }
  }
  return false;
}
