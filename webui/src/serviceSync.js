import svc from '../../scripts/serviceSync.js';

export async function serviceSync({ db, url, services = [] } = {}, helpers = {}) {
  const args = [];
  if (db) {
    args.push('--db', db);
    if (url) args.push('--url', url);
  }
  if (url && !db) {
    args.push('--url', url);
  }
  if (services.length) {
    args.push('--services', ...services);
  }
  return await svc.run(args, helpers);
}
