export class HealthMonitor {
  constructor(scheduler, interval = 10, collector = null) {
    this.scheduler = scheduler;
    this.interval = interval;
    this.collector = collector || { collect: async () => ({}) };
    this.data = null;
    scheduler.schedule('health_monitor', () => this._poll(), interval);
  }

  async _poll() {
    try {
      this.data = await this.collector.collect();
    } catch (_) {
      this.data = null;
    }
  }
}
