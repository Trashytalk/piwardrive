# State Management Implementation Plan

## Implementation with Context API and React Hooks

### Step 1: Create Core State Contexts

Create a directory structure for organized state management:

```bash
mkdir -p webui/src/state/contexts
mkdir -p webui/src/state/providers
mkdir -p webui/src/state/hooks
```

### Step 2: Define Application State Contexts

```jsx
// webui/src/state/contexts/AppStateContext.jsx

import { createContext } from 'react';

// Define initial state
export const initialAppState = {
  status: [],
  metrics: null,
  logs: '',
  plugins: [],
  widgets: [],
  orientationData: null,
  vehicleData: null,
  configData: null,
  error: null,
  isLoading: false
};

// Create context with initial state
export const AppStateContext = createContext(initialAppState);

// Create update context
export const AppDispatchContext = createContext(null);
```

### Step 3: Create Provider Component

```jsx
// webui/src/state/providers/AppStateProvider.jsx

import { useReducer } from 'react';
import { AppStateContext, AppDispatchContext, initialAppState } from '../contexts/AppStateContext';

// Define action types
export const ActionTypes = {
  SET_STATUS: 'SET_STATUS',
  SET_METRICS: 'SET_METRICS',
  SET_LOGS: 'SET_LOGS',
  SET_PLUGINS: 'SET_PLUGINS',
  SET_WIDGETS: 'SET_WIDGETS',
  SET_ORIENTATION_DATA: 'SET_ORIENTATION_DATA',
  SET_VEHICLE_DATA: 'SET_VEHICLE_DATA',
  SET_CONFIG_DATA: 'SET_CONFIG_DATA',
  SET_ERROR: 'SET_ERROR',
  SET_LOADING: 'SET_LOADING',
  CLEAR_ERROR: 'CLEAR_ERROR'
};

// Define reducer function
function appReducer(state, action) {
  switch (action.type) {
    case ActionTypes.SET_STATUS:
      return { ...state, status: action.payload };
    case ActionTypes.SET_METRICS:
      return { ...state, metrics: action.payload };
    case ActionTypes.SET_LOGS:
      return { ...state, logs: action.payload };
    case ActionTypes.SET_PLUGINS:
      return { ...state, plugins: action.payload };
    case ActionTypes.SET_WIDGETS:
      return { ...state, widgets: action.payload };
    case ActionTypes.SET_ORIENTATION_DATA:
      return { ...state, orientationData: action.payload };
    case ActionTypes.SET_VEHICLE_DATA:
      return { ...state, vehicleData: action.payload };
    case ActionTypes.SET_CONFIG_DATA:
      return { ...state, configData: action.payload };
    case ActionTypes.SET_ERROR:
      return { ...state, error: action.payload };
    case ActionTypes.SET_LOADING:
      return { ...state, isLoading: action.payload };
    case ActionTypes.CLEAR_ERROR:
      return { ...state, error: null };
    default:
      return state;
  }
}

// Provider component
export function AppStateProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialAppState);
  
  return (
    <AppStateContext.Provider value={state}>
      <AppDispatchContext.Provider value={dispatch}>
        {children}
      </AppDispatchContext.Provider>
    </AppStateContext.Provider>
  );
}
```

### Step 4: Create Custom Hooks for State Access

```jsx
// webui/src/state/hooks/useAppState.jsx

import { useContext } from 'react';
import { AppStateContext } from '../contexts/AppStateContext';

export function useAppState() {
  const context = useContext(AppStateContext);
  
  if (context === undefined) {
    throw new Error('useAppState must be used within an AppStateProvider');
  }
  
  return context;
}
```

```jsx
// webui/src/state/hooks/useAppDispatch.jsx

import { useContext } from 'react';
import { AppDispatchContext } from '../contexts/AppStateContext';
import { ActionTypes } from '../providers/AppStateProvider';

export function useAppDispatch() {
  const dispatch = useContext(AppDispatchContext);
  
  if (dispatch === undefined) {
    throw new Error('useAppDispatch must be used within an AppStateProvider');
  }
  
  // Provide action creators
  const setStatus = (status) => dispatch({ type: ActionTypes.SET_STATUS, payload: status });
  const setMetrics = (metrics) => dispatch({ type: ActionTypes.SET_METRICS, payload: metrics });
  const setLogs = (logs) => dispatch({ type: ActionTypes.SET_LOGS, payload: logs });
  const setPlugins = (plugins) => dispatch({ type: ActionTypes.SET_PLUGINS, payload: plugins });
  const setWidgets = (widgets) => dispatch({ type: ActionTypes.SET_WIDGETS, payload: widgets });
  const setOrientationData = (data) => dispatch({ type: ActionTypes.SET_ORIENTATION_DATA, payload: data });
  const setVehicleData = (data) => dispatch({ type: ActionTypes.SET_VEHICLE_DATA, payload: data });
  const setConfigData = (data) => dispatch({ type: ActionTypes.SET_CONFIG_DATA, payload: data });
  const setError = (error) => dispatch({ type: ActionTypes.SET_ERROR, payload: error });
  const setLoading = (isLoading) => dispatch({ type: ActionTypes.SET_LOADING, payload: isLoading });
  const clearError = () => dispatch({ type: ActionTypes.CLEAR_ERROR });
  
  return {
    setStatus,
    setMetrics,
    setLogs,
    setPlugins,
    setWidgets,
    setOrientationData,
    setVehicleData,
    setConfigData,
    setError,
    setLoading,
    clearError
  };
}
```

### Step 5: Create API Integration Hooks

```jsx
// webui/src/state/hooks/useApiData.jsx

import { useEffect } from 'react';
import { useAppDispatch } from './useAppDispatch';
import { reportError } from '../../exceptionHandler';

export function useApiData(endpoint, actionCreator, dependencies = []) {
  const { setLoading, setError } = useAppDispatch();
  
  useEffect(() => {
    let isMounted = true;
    
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await fetch(endpoint);
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        if (isMounted) {
          actionCreator(data);
        }
      } catch (error) {
        if (isMounted) {
          setError(error.message);
          reportError(error);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };
    
    fetchData();
    
    return () => {
      isMounted = false;
    };
  }, dependencies);
}
```

### Step 6: Create WebSocket Integration Hook

```jsx
// webui/src/state/hooks/useWebSocketData.jsx

import { useEffect } from 'react';
import { useAppDispatch } from './useAppDispatch';
import { reportError } from '../../exceptionHandler';

export function useWebSocketData(url, handlers = {}) {
  const { setError } = useAppDispatch();
  
  useEffect(() => {
    const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    let ws;
    let ping;
    let reconnectTimer;
    
    const connect = () => {
      ws = new WebSocket(`${proto}//${window.location.host}${url}`);
      
      ws.onopen = () => {
        if (ping) clearInterval(ping);
        ping = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send('ping');
          }
        }, 15000);
        
        if (handlers.onOpen) handlers.onOpen();
      };
      
      ws.onmessage = (ev) => {
        try {
          const data = JSON.parse(ev.data);
          
          // Handle different data types
          if (data.status && handlers.onStatus) {
            handlers.onStatus(data.status);
          }
          
          if (data.metrics && handlers.onMetrics) {
            handlers.onMetrics(data.metrics);
          }
          
          if (handlers.onMessage) {
            handlers.onMessage(data);
          }
        } catch (e) {
          reportError(e);
        }
      };
      
      ws.onerror = (error) => {
        setError(`WebSocket error: ${error}`);
        ws.close();
      };
      
      ws.onclose = () => {
        if (ping) {
          clearInterval(ping);
          ping = null;
        }
        
        if (handlers.onClose) handlers.onClose();
        
        // Reconnect logic
        reconnectTimer = setTimeout(() => {
          if (window.WebSocket) {
            connect();
          } else if (handlers.onFallback) {
            handlers.onFallback();
          }
        }, 3000);
      };
    };
    
    connect();
    
    return () => {
      if (ws) {
        ws.close();
      }
      if (ping) {
        clearInterval(ping);
      }
      if (reconnectTimer) {
        clearTimeout(reconnectTimer);
      }
    };
  }, [url]);
}
```

### Step 7: Update Main App Component

```jsx
// webui/src/App.jsx - Updated with state management

import { useEffect } from 'react';
import { AppStateProvider } from './state/providers/AppStateProvider';
import { useAppState } from './state/hooks/useAppState';
import { useAppDispatch } from './state/hooks/useAppDispatch';
import { useWebSocketData } from './state/hooks/useWebSocketData';
import { useApiData } from './state/hooks/useApiData';

import BatteryStatus from './components/BatteryStatus';
import ServiceStatus from './components/ServiceStatus';
// ...other imports

function AppContent() {
  const { 
    status, 
    metrics, 
    logs, 
    plugins, 
    widgets, 
    orientationData, 
    vehicleData, 
    configData
  } = useAppState();
  
  const { 
    setStatus, 
    setMetrics, 
    setPlugins, 
    setWidgets, 
    setConfigData 
  } = useAppDispatch();
  
  // Load initial data
  useApiData('/api/plugins', setPlugins, []);
  useApiData('/api/widgets', setWidgets, []);
  useApiData('/api/config', setConfigData, []);
  
  // Setup WebSocket connection
  useWebSocketData('/ws/status', {
    onStatus: setStatus,
    onMetrics: setMetrics
  });
  
  const handleConfigChange = (key, value) => {
    setConfigData({ ...configData, [key]: value });
  };
  
  const saveConfig = async () => {
    try {
      const response = await fetch('/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(configData),
      });
      
      if (!response.ok) {
        throw new Error(`Config save failed: ${response.status}`);
      }
      
      const updatedConfig = await response.json();
      setConfigData(updatedConfig);
    } catch (error) {
      // Error handling
    }
  };
  
  return (
    <div className="app-container">
      {/* Main UI components using state values */}
      <ServiceStatus status={status} />
      {metrics && <NetworkThroughput metrics={metrics.network} />}
      {/* ...other components */}
    </div>
  );
}

export default function App() {
  return (
    <AppStateProvider>
      <AppContent />
    </AppStateProvider>
  );
}
```

### Step 8: Component Refactoring Example

```jsx
// Before: webui/src/components/ServiceStatus.jsx
import React from 'react';

export default function ServiceStatus({ status }) {
  return (
    <div className="service-status">
      {status.map(s => (
        <div key={s.id} className={`status-item ${s.status}`}>
          {s.id}: {s.status}
        </div>
      ))}
    </div>
  );
}

// After: webui/src/components/ServiceStatus.jsx
import React from 'react';
import { useAppState } from '../state/hooks/useAppState';

export default function ServiceStatus() {
  const { status } = useAppState();
  
  return (
    <div className="service-status">
      {status.map(s => (
        <div key={s.id} className={`status-item ${s.status}`}>
          {s.id}: {s.status}
        </div>
      ))}
    </div>
  );
}
```

## Advanced Features Implementation (Optional)

### Middleware for Logging/Debugging

```jsx
// webui/src/state/middlewares/loggingMiddleware.jsx
export const withLogging = (dispatch) => (action) => {
  console.log('Dispatching action:', action);
  const result = dispatch(action);
  return result;
};

// Add to provider:
const [state, baseDispatch] = useReducer(appReducer, initialAppState);
const dispatch = withLogging(baseDispatch);
```

### Persist State to LocalStorage

```jsx
// webui/src/state/utils/persistState.jsx
export const saveState = (state) => {
  try {
    const serializedState = JSON.stringify(state);
    localStorage.setItem('piwardrive_state', serializedState);
  } catch (err) {
    console.error('Could not save state', err);
  }
};

export const loadState = () => {
  try {
    const serializedState = localStorage.getItem('piwardrive_state');
    if (!serializedState) return undefined;
    return JSON.parse(serializedState);
  } catch (err) {
    console.error('Could not load state', err);
    return undefined;
  }
};
```
