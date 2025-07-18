# TypeScript Migration Plan

## Phase 1: Setup and Configuration
1. Install TypeScript and related dependencies:
```bash
cd webui
npm install --save-dev typescript @types/react @types/react-dom @types/leaflet @types/chart.js @types/react-router-dom
```

2. Create a basic `tsconfig.json` file in the webui directory:
```json
{
  "compilerOptions": {
    "target": "ESNext",
    "useDefineForClassFields": true,
    "lib": ["DOM", "DOM.Iterable", "ESNext"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "module": "ESNext",
    "moduleResolution": "Node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

3. Create a `tsconfig.node.json` file:
```json
{
  "compilerOptions": {
    "composite": true,
    "module": "ESNext",
    "moduleResolution": "Node",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
```

4. Update Vite configuration to support TypeScript by renaming `vite.config.js` to `vite.config.ts`

## Phase 2: Create Type Definitions

1. Create a `src/types` directory for shared type definitions:
```bash
mkdir -p webui/src/types
```

2. Create API interface definitions based on backend endpoints:
```typescript
// webui/src/types/api.ts
export interface Status {
  id: string;
  status: 'running' | 'stopped' | 'error';
  timestamp: string;
  details?: string;
}

export interface Metrics {
  cpu: number;
  memory: number;
  disk: number;
  network: {
    rx: number;
    tx: number;
  };
  temperature: number;
  battery?: {
    level: number;
    charging: boolean;
  };
}

export interface OrientationData {
  pitch: number;
  roll: number;
  yaw: number;
  timestamp: string;
}

export interface VehicleData {
  speed: number;
  heading: number;
  altitude: number;
  timestamp: string;
}

export interface ConfigData {
  [key: string]: any;
}

export interface Widget {
  id: string;
  name: string;
  description: string;
  component: string;
}
```

## Phase 3: Migrate Core Components

Begin migrating components one by one, starting with simpler utility functions:

1. Rename `.js` files to `.tsx` or `.ts` as appropriate
2. Add type annotations to functions and variables
3. Update imports and fix type errors

Example migration for a utility file:

```typescript
// From: useWebSocket.js
// To: useWebSocket.ts
import { useEffect, useState } from 'react';
import { reportError } from './exceptionHandler';

interface WebSocketOptions {
  onMessage?: (data: any) => void;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: Event) => void;
  reconnectInterval?: number;
}

export function useWebSocket(url: string, options: WebSocketOptions = {}) {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<any>(null);

  useEffect(() => {
    let ws: WebSocket;
    let reconnectTimer: number;

    const connect = () => {
      ws = new WebSocket(url);

      ws.onopen = () => {
        setIsConnected(true);
        if (options.onOpen) options.onOpen();
      };

      ws.onclose = () => {
        setIsConnected(false);
        if (options.onClose) options.onClose();
        
        // Reconnect logic
        reconnectTimer = window.setTimeout(
          connect, 
          options.reconnectInterval || 3000
        );
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setLastMessage(data);
          if (options.onMessage) options.onMessage(data);
        } catch (error) {
          reportError(error);
        }
      };

      ws.onerror = (error) => {
        if (options.onError) options.onError(error);
      };

      setSocket(ws);
    };

    connect();

    return () => {
      if (ws) {
        ws.close();
      }
      if (reconnectTimer) {
        clearTimeout(reconnectTimer);
      }
    };
  }, [url]);

  const sendMessage = (data: any) => {
    if (socket && isConnected) {
      socket.send(JSON.stringify(data));
    }
  };

  return { isConnected, lastMessage, sendMessage };
}
```

## Phase 4: Create Component Type Props

For each React component, define proper prop types:

```typescript
// Example for BatteryStatus.tsx
import React from 'react';

interface BatteryStatusProps {
  level: number;
  charging: boolean;
  lowThreshold?: number;
}

const BatteryStatus: React.FC<BatteryStatusProps> = ({
  level,
  charging,
  lowThreshold = 20
}) => {
  // Component implementation
};

export default BatteryStatus;
```

## Phase 5: Migrate Complex Components and App Structure

1. Migrate the main App component with proper typing
2. Update the state management with proper TypeScript types

## Phase 6: Testing and Validation

1. Update test files to TypeScript
2. Run type checking as part of CI/CD process
3. Add type coverage reporting

## Phase 7: Documentation and Standards

1. Document TypeScript coding standards
2. Update contribution guidelines
3. Ensure all new code follows TypeScript patterns
