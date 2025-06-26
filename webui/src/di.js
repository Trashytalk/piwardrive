export class Container {
  constructor() {
    this.instances = new Map();
    this.factories = new Map();
  }

  registerInstance(key, instance) {
    this.instances.set(key, instance);
  }

  registerFactory(key, factory) {
    this.factories.set(key, factory);
  }

  has(key) {
    return this.instances.has(key) || this.factories.has(key);
  }

  resolve(key) {
    if (this.instances.has(key)) {
      return this.instances.get(key);
    }
    if (this.factories.has(key)) {
      const inst = this.factories.get(key)();
      this.instances.set(key, inst);
      return inst;
    }
    throw new Error(`No provider for ${key}`);
  }
}
