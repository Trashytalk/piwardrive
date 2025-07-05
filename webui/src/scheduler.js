export class PollScheduler {
  constructor() {
    this.intervals = new Map();
    this.metrics = new Map();
  }

  schedule(name, cb, interval) {
    this.cancel(name);
    const run = () => {
      const start = performance.now();
      Promise.resolve(
        cb(
          (Date.now() - (this.metrics.get(name)?.lastRun || Date.now())) / 1000
        )
      ).finally(() => {
        const m = this.metrics.get(name);
        if (m) {
          m.lastDuration = (performance.now() - start) / 1000;
          m.nextRun = Date.now() + interval * 1000;
          m.lastRun = Date.now();
        }
      });
    };
    this.metrics.set(name, {
      nextRun: Date.now() + interval * 1000,
      lastDuration: NaN,
      lastRun: Date.now(),
    });
    this.intervals.set(name, setInterval(run, interval * 1000));
  }

  registerWidget(widget, name = null) {
    const interval = widget.update_interval;
    const cbName = name || widget.constructor.name;
    this.schedule(cbName, (dt) => widget.update(dt), interval);
  }

  cancel(name) {
    const id = this.intervals.get(name);
    if (id) clearInterval(id);
    this.intervals.delete(name);
    this.metrics.delete(name);
  }

  cancelAll() {
    Array.from(this.intervals.keys()).forEach((name) => this.cancel(name));
  }

  getMetrics() {
    const out = {};
    for (const [k, v] of this.metrics.entries()) {
      out[k] = { next_run: v.nextRun, last_duration: v.lastDuration };
    }
    return out;
  }
}

export class AsyncScheduler {
  constructor() {
    this.timers = new Map();
    this.metrics = new Map();
  }

  schedule(name, cb, interval) {
    this.cancel(name);
    const run = async () => {
      const start = performance.now();
      try {
        await cb();
      } finally {
        const m = this.metrics.get(name);
        if (m) {
          m.lastDuration = (performance.now() - start) / 1000;
          m.nextRun = Date.now() + interval * 1000;
          this.timers.set(name, setTimeout(run, interval * 1000));
        }
      }
    };
    this.metrics.set(name, {
      nextRun: Date.now() + interval * 1000,
      lastDuration: NaN,
    });
    this.timers.set(name, setTimeout(run, interval * 1000));
  }

  registerWidget(widget, name = null) {
    const interval = widget.update_interval;
    const cbName = name || widget.constructor.name;
    this.schedule(cbName, () => widget.update(), interval);
  }

  cancel(name) {
    const id = this.timers.get(name);
    if (id) clearTimeout(id);
    this.timers.delete(name);
    this.metrics.delete(name);
  }

  async cancelAll() {
    for (const name of Array.from(this.timers.keys())) {
      this.cancel(name);
    }
  }

  getMetrics() {
    const out = {};
    for (const [k, v] of this.metrics.entries()) {
      out[k] = { next_run: v.nextRun, last_duration: v.lastDuration };
    }
    return out;
  }
}
