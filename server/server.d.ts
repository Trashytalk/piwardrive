export interface ServerOptions {
  distDir?: string;
  healthFile?: string;
}

export function verifyPassword(password: string, hashed: string): boolean;

export type BasicAuthHandler = (
  req: any,
  res: any,
  next: (err?: any) => void
) => void;

export const basicAuth: BasicAuthHandler;

export function parseWidgets(): string[];

export function createServer(options?: ServerOptions): any;
