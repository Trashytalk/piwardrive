export type Factory<T> = () => T;

export class Container {
  private instances = new Map<string, unknown>();
  private factories = new Map<string, Factory<unknown>>();

  registerInstance<T>(key: string, instance: T): void {
    this.instances.set(key, instance);
  }

  registerFactory<T>(key: string, factory: Factory<T>): void {
    this.factories.set(key, factory as Factory<unknown>);
  }

  has(key: string): boolean {
    return this.instances.has(key) || this.factories.has(key);
  }

  resolve<T>(key: string): T {
    if (this.instances.has(key)) {
      return this.instances.get(key) as T;
    }
    if (this.factories.has(key)) {
      const factory = this.factories.get(key) as Factory<T>;
      const inst = factory();
      this.instances.set(key, inst);
      return inst;
    }
    throw new Error(`No provider for ${key}`);
  }
}
