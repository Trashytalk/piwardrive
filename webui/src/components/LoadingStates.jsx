import React from 'react';

export function LoadingSpinner({ size = 'medium', message = 'Loading...' }) {
  const sizeClasses = {
    small: 'loading-spinner-small',
    medium: 'loading-spinner-medium',
    large: 'loading-spinner-large'
  };

  return (
    <div className="loading-spinner-container">
      <div className={`loading-spinner ${sizeClasses[size]}`}>
        <div className="spinner"></div>
      </div>
      {message && <div className="loading-message">{message}</div>}
    </div>
  );
}

export function LoadingOverlay({ isLoading, children, message = 'Loading...' }) {
  if (!isLoading) {
    return children;
  }

  return (
    <div className="loading-overlay-container">
      <div className="loading-overlay">
        <LoadingSpinner size="large" message={message} />
      </div>
      <div className="loading-content">{children}</div>
    </div>
  );
}

export function SkeletonLoader({ type = 'text', count = 1 }) {
  const skeletonElements = Array.from({ length: count }, (_, index) => (
    <div key={index} className={`skeleton skeleton-${type}`}></div>
  ));

  return <div className="skeleton-container">{skeletonElements}</div>;
}

// Hook for managing loading states
export function useLoading(initialState = false) {
  const [isLoading, setIsLoading] = React.useState(initialState);
  const [error, setError] = React.useState(null);

  const startLoading = React.useCallback(() => {
    setIsLoading(true);
    setError(null);
  }, []);

  const stopLoading = React.useCallback(() => {
    setIsLoading(false);
  }, []);

  const setLoadingError = React.useCallback((error) => {
    setIsLoading(false);
    setError(error);
  }, []);

  const reset = React.useCallback(() => {
    setIsLoading(false);
    setError(null);
  }, []);

  return {
    isLoading,
    error,
    startLoading,
    stopLoading,
    setLoadingError,
    reset
  };
}

export default LoadingSpinner;
