import React from 'react';
import { reportError } from '../exceptionHandler.js';

export class NetworkError extends Error {
  constructor(message, status, response) {
    super(message);
    this.name = 'NetworkError';
    this.status = status;
    this.response = response;
  }
}

export class TimeoutError extends Error {
  constructor(message = 'Request timed out') {
    super(message);
    this.name = 'TimeoutError';
  }
}

export class ConnectionError extends Error {
  constructor(message = 'Connection failed') {
    super(message);
    this.name = 'ConnectionError';
  }
}

// Enhanced fetch with error handling, retries, and timeouts
export async function enhancedFetch(url, options = {}) {
  const {
    timeout = 10000,
    retries = 3,
    retryDelay = 1000,
    ...fetchOptions
  } = options;

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);

      const response = await fetch(url, {
        ...fetchOptions,
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorMessage = `HTTP ${response.status}: ${response.statusText}`;
        throw new NetworkError(errorMessage, response.status, response);
      }

      return response;

    } catch (error) {
      const isLastAttempt = attempt === retries;

      if (error.name === 'AbortError') {
        const timeoutError = new TimeoutError(`Request timed out after ${timeout}ms`);
        if (isLastAttempt) {
          reportError(timeoutError);
          throw timeoutError;
        }
      } else if (error instanceof NetworkError) {
        if (isLastAttempt || error.status < 500) {
          reportError(error);
          throw error;
        }
      } else {
        const connectionError = new ConnectionError(`Network request failed: ${error.message}`);
        if (isLastAttempt) {
          reportError(connectionError);
          throw connectionError;
        }
      }

      // Wait before retrying (exponential backoff)
      if (!isLastAttempt) {
        await new Promise(resolve => setTimeout(resolve, retryDelay * Math.pow(2, attempt)));
      }
    }
  }
}

// Hook for API calls with error handling
export function useApiCall() {
  const [state, setState] = React.useState({
    data: null,
    loading: false,
    error: null
  });

  const execute = React.useCallback(async (apiCall) => {
    setState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const data = await apiCall();
      setState({ data, loading: false, error: null });
      return data;
    } catch (error) {
      setState(prev => ({ ...prev, loading: false, error }));
      throw error;
    }
  }, []);

  const reset = React.useCallback(() => {
    setState({ data: null, loading: false, error: null });
  }, []);

  return { ...state, execute, reset };
}

// Centralized error handler for different error types
export function handleApiError(error, context = '') {
  let userMessage = 'An unexpected error occurred';
  let shouldRetry = false;
  let isTemporary = false;

  if (error instanceof NetworkError) {
    switch (error.status) {
      case 400:
        userMessage = 'Bad request. Please check your input and try again.';
        break;
      case 401:
        userMessage = 'Authentication required. Please log in again.';
        // Redirect to login if needed
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
        break;
      case 403:
        userMessage = 'Access denied. You don\'t have permission for this action.';
        break;
      case 404:
        userMessage = 'Resource not found. The requested item may have been deleted.';
        break;
      case 429:
        userMessage = 'Too many requests. Please wait a moment and try again.';
        shouldRetry = true;
        isTemporary = true;
        break;
      case 500:
      case 502:
      case 503:
      case 504:
        userMessage = 'Server error. Please try again in a few moments.';
        shouldRetry = true;
        isTemporary = true;
        break;
      default:
        userMessage = `Network error (${error.status}). Please try again.`;
        shouldRetry = error.status >= 500;
        isTemporary = error.status >= 500;
    }
  } else if (error instanceof TimeoutError) {
    userMessage = 'Request timed out. Please check your connection and try again.';
    shouldRetry = true;
    isTemporary = true;
  } else if (error instanceof ConnectionError) {
    userMessage = 'Connection failed. Please check your internet connection.';
    shouldRetry = true;
    isTemporary = true;
  } else {
    userMessage = error.message || 'An unexpected error occurred';
  }

  // Add context if provided
  if (context) {
    userMessage = `${context}: ${userMessage}`;
  }

  return {
    message: userMessage,
    shouldRetry,
    isTemporary,
    originalError: error
  };
}

// Connection status monitoring
export function useConnectionStatus() {
  const [isOnline, setIsOnline] = React.useState(navigator.onLine);
  const [connectionQuality, setConnectionQuality] = React.useState('unknown');

  React.useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Monitor connection quality
    if ('connection' in navigator) {
      const connection = navigator.connection;
      const updateConnectionQuality = () => {
        setConnectionQuality(connection.effectiveType || 'unknown');
      };
      connection.addEventListener('change', updateConnectionQuality);
      updateConnectionQuality();
    }

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return { isOnline, connectionQuality };
}

export default enhancedFetch;
