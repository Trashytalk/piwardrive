import React from 'react';
import { handleApiError } from '../utils/networkErrorHandler.js';

export function ErrorDisplay({ error, onRetry, onDismiss, context = '' }) {
  if (!error) return null;

  const errorInfo = handleApiError(error, context);

  return (
    <div className={`error-display ${errorInfo.isTemporary ? 'error-temporary' : 'error-permanent'}`}>
      <div className="error-content">
        <div className="error-icon">
          {errorInfo.isTemporary ? '⚠️' : '❌'}
        </div>
        <div className="error-message">
          <strong>Error:</strong> {errorInfo.message}
        </div>
        <div className="error-actions">
          {errorInfo.shouldRetry && onRetry && (
            <button onClick={onRetry} className="btn btn-primary btn-sm">
              Try Again
            </button>
          )}
          {onDismiss && (
            <button onClick={onDismiss} className="btn btn-secondary btn-sm">
              Dismiss
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export function InlineError({ error, prefix = 'Error: ' }) {
  if (!error) return null;

  const errorInfo = handleApiError(error);

  return (
    <div className="inline-error">
      <span className="error-icon">⚠️</span>
      <span className="error-text">{prefix}{errorInfo.message}</span>
    </div>
  );
}

export function ConnectionStatus() {
  const [isOnline, setIsOnline] = React.useState(navigator.onLine);
  const [showStatus, setShowStatus] = React.useState(false);

  React.useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      setShowStatus(true);
      setTimeout(() => setShowStatus(false), 3000);
    };

    const handleOffline = () => {
      setIsOnline(false);
      setShowStatus(true);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  if (!showStatus && isOnline) return null;

  return (
    <div className={`connection-status ${isOnline ? 'online' : 'offline'}`}>
      <div className="connection-content">
        <span className="connection-icon">
          {isOnline ? '🟢' : '🔴'}
        </span>
        <span className="connection-text">
          {isOnline ? 'Connection restored' : 'No internet connection'}
        </span>
      </div>
    </div>
  );
}

export function NotificationToast({ notifications, onDismiss }) {
  if (!notifications || notifications.length === 0) return null;

  return (
    <div className="notification-toast-container">
      {notifications.map((notification, index) => (
        <div
          key={notification.id || index}
          className={`notification-toast notification-${notification.type || 'info'}`}
        >
          <div className="notification-content">
            <div className="notification-icon">
              {notification.type === 'error' && '❌'}
              {notification.type === 'warning' && '⚠️'}
              {notification.type === 'success' && '✅'}
              {notification.type === 'info' && 'ℹ️'}
            </div>
            <div className="notification-message">
              {notification.title && (
                <div className="notification-title">{notification.title}</div>
              )}
              <div className="notification-text">{notification.message}</div>
            </div>
            {onDismiss && (
              <button
                onClick={() => onDismiss(notification.id || index)}
                className="notification-dismiss"
              >
                ×
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

// Hook for managing notifications
export function useNotifications() {
  const [notifications, setNotifications] = React.useState([]);

  const addNotification = React.useCallback((notification) => {
    const id = Date.now() + Math.random();
    const newNotification = { ...notification, id };
    
    setNotifications(prev => [...prev, newNotification]);

    // Auto-dismiss after timeout
    if (notification.autoHide !== false) {
      const timeout = notification.timeout || 5000;
      setTimeout(() => {
        setNotifications(prev => prev.filter(n => n.id !== id));
      }, timeout);
    }

    return id;
  }, []);

  const removeNotification = React.useCallback((id) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  }, []);

  const clearAll = React.useCallback(() => {
    setNotifications([]);
  }, []);

  const addError = React.useCallback((message, title = 'Error') => {
    return addNotification({ type: 'error', title, message });
  }, [addNotification]);

  const addWarning = React.useCallback((message, title = 'Warning') => {
    return addNotification({ type: 'warning', title, message });
  }, [addNotification]);

  const addSuccess = React.useCallback((message, title = 'Success') => {
    return addNotification({ type: 'success', title, message });
  }, [addNotification]);

  const addInfo = React.useCallback((message, title = 'Info') => {
    return addNotification({ type: 'info', title, message });
  }, [addNotification]);

  return {
    notifications,
    addNotification,
    removeNotification,
    clearAll,
    addError,
    addWarning,
    addSuccess,
    addInfo
  };
}

export default ErrorDisplay;
