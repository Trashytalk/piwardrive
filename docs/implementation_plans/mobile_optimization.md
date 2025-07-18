# Mobile Optimization Implementation Plan

## Overview

This plan outlines the implementation of comprehensive mobile optimization for the PiWardrive web application, focusing on responsive design, touch-friendly interfaces, offline capabilities, and Progressive Web App (PWA) features for field operations.

## Phase 1: Responsive Design Foundation

### Step 1: Mobile-First CSS Framework

Create a responsive CSS framework tailored for PiWardrive's specific needs:

```css
/* webui/src/styles/responsive.css */

/* Mobile-first approach with progressive enhancement */
:root {
  --mobile-breakpoint: 768px;
  --tablet-breakpoint: 1024px;
  --desktop-breakpoint: 1200px;
  
  /* Touch-friendly sizing */
  --touch-target-min: 44px;
  --touch-spacing: 8px;
  
  /* Mobile-optimized typography */
  --mobile-font-size: 16px;
  --mobile-line-height: 1.5;
  --mobile-heading-scale: 1.25;
}

/* Base styles (mobile-first) */
* {
  box-sizing: border-box;
}

body {
  font-size: var(--mobile-font-size);
  line-height: var(--mobile-line-height);
  margin: 0;
  padding: 0;
  -webkit-text-size-adjust: 100%;
  -ms-text-size-adjust: 100%;
}

/* Touch-friendly buttons */
button, .btn {
  min-height: var(--touch-target-min);
  min-width: var(--touch-target-min);
  padding: 12px 16px;
  margin: var(--touch-spacing);
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  user-select: none;
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}

/* Touch-friendly form inputs */
input, select, textarea {
  min-height: var(--touch-target-min);
  padding: 12px 16px;
  font-size: 16px; /* Prevents zoom on iOS */
  border: 1px solid #ddd;
  border-radius: 8px;
  margin: var(--touch-spacing) 0;
  width: 100%;
  max-width: 100%;
}

/* Responsive grid system */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

.row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -8px;
}

.col {
  flex: 1;
  padding: 0 8px;
  min-width: 0;
}

/* Mobile-specific columns */
.col-mobile-12 { width: 100%; }
.col-mobile-6 { width: 50%; }
.col-mobile-4 { width: 33.333%; }
.col-mobile-3 { width: 25%; }

/* Tablet styles */
@media (min-width: 768px) {
  .col-tablet-12 { width: 100%; }
  .col-tablet-6 { width: 50%; }
  .col-tablet-4 { width: 33.333%; }
  .col-tablet-3 { width: 25%; }
  
  .container {
    padding: 0 24px;
  }
}

/* Desktop styles */
@media (min-width: 1024px) {
  .col-desktop-12 { width: 100%; }
  .col-desktop-6 { width: 50%; }
  .col-desktop-4 { width: 33.333%; }
  .col-desktop-3 { width: 25%; }
  .col-desktop-2 { width: 16.666%; }
  
  .container {
    padding: 0 32px;
  }
}

/* Mobile navigation */
.mobile-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-around;
  padding: 8px 0;
  z-index: 1000;
}

.mobile-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 12px;
  text-decoration: none;
  color: #666;
  min-width: var(--touch-target-min);
}

.mobile-nav-item.active {
  color: #007bff;
}

.mobile-nav-icon {
  font-size: 20px;
  margin-bottom: 4px;
}

.mobile-nav-label {
  font-size: 12px;
}

/* Hide mobile nav on desktop */
@media (min-width: 1024px) {
  .mobile-nav {
    display: none;
  }
}

/* Responsive tables */
.table-responsive {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  margin-bottom: 16px;
}

.table-responsive table {
  min-width: 600px;
}

/* Mobile-optimized cards */
.card-mobile {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin: 16px 0;
  overflow: hidden;
}

.card-mobile-header {
  padding: 16px;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.card-mobile-content {
  padding: 16px;
}

.card-mobile-actions {
  padding: 16px;
  background: #f8f9fa;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Loading states */
.loading-spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #007bff;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 20px auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Mobile-specific utilities */
.mobile-only {
  display: block;
}

.desktop-only {
  display: none;
}

@media (min-width: 1024px) {
  .mobile-only {
    display: none;
  }
  
  .desktop-only {
    display: block;
  }
}

/* Swipe gestures */
.swipe-container {
  overflow: hidden;
  position: relative;
}

.swipe-item {
  transition: transform 0.3s ease;
}

/* Pull-to-refresh */
.pull-to-refresh {
  position: relative;
  overflow: hidden;
}

.pull-to-refresh-indicator {
  position: absolute;
  top: -50px;
  left: 50%;
  transform: translateX(-50%);
  transition: top 0.3s ease;
}

.pull-to-refresh-indicator.visible {
  top: 20px;
}
```

### Step 2: Mobile-Optimized Components

Create responsive React components:

```jsx
// webui/src/components/MobileLayout.jsx

import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const MobileLayout = ({ children }) => {
  const [isMobile, setIsMobile] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const navigationItems = [
    { path: '/', icon: '🏠', label: 'Home' },
    { path: '/scan', icon: '📡', label: 'Scan' },
    { path: '/map', icon: '🗺️', label: 'Map' },
    { path: '/settings', icon: '⚙️', label: 'Settings' }
  ];

  return (
    <div className="mobile-layout">
      <main className="mobile-content">
        {children}
      </main>
      
      {isMobile && (
        <nav className="mobile-nav">
          {navigationItems.map((item) => (
            <a
              key={item.path}
              href={item.path}
              className={`mobile-nav-item ${location.pathname === item.path ? 'active' : ''}`}
            >
              <span className="mobile-nav-icon">{item.icon}</span>
              <span className="mobile-nav-label">{item.label}</span>
            </a>
          ))}
        </nav>
      )}
    </div>
  );
};

export default MobileLayout;
```

```jsx
// webui/src/components/MobileStatusCard.jsx

import React from 'react';

const MobileStatusCard = ({ title, value, status, icon, onClick }) => {
  return (
    <div className="card-mobile" onClick={onClick}>
      <div className="card-mobile-header">
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <span style={{ fontSize: '24px', marginRight: '12px' }}>{icon}</span>
          <h3 style={{ margin: 0, fontSize: '18px' }}>{title}</h3>
        </div>
      </div>
      <div className="card-mobile-content">
        <div style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '8px' }}>
          {value}
        </div>
        <div style={{ 
          fontSize: '14px', 
          color: status === 'active' ? '#28a745' : '#dc3545',
          display: 'flex',
          alignItems: 'center'
        }}>
          <span style={{ 
            width: '8px', 
            height: '8px', 
            borderRadius: '50%', 
            backgroundColor: status === 'active' ? '#28a745' : '#dc3545',
            marginRight: '8px'
          }}></span>
          {status === 'active' ? 'Active' : 'Inactive'}
        </div>
      </div>
    </div>
  );
};

export default MobileStatusCard;
```

## Phase 2: Touch-Friendly Interface

### Step 1: Touch Gesture Handler

```jsx
// webui/src/hooks/useTouch.js

import { useState, useEffect } from 'react';

export const useTouch = (element) => {
  const [touchData, setTouchData] = useState({
    startX: 0,
    startY: 0,
    currentX: 0,
    currentY: 0,
    deltaX: 0,
    deltaY: 0,
    direction: null,
    velocity: 0,
    isSwiping: false
  });

  useEffect(() => {
    if (!element) return;

    let startTime = 0;
    let startX = 0;
    let startY = 0;

    const handleTouchStart = (e) => {
      startTime = Date.now();
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
      
      setTouchData(prev => ({
        ...prev,
        startX,
        startY,
        currentX: startX,
        currentY: startY,
        isSwiping: false
      }));
    };

    const handleTouchMove = (e) => {
      const currentX = e.touches[0].clientX;
      const currentY = e.touches[0].clientY;
      const deltaX = currentX - startX;
      const deltaY = currentY - startY;
      
      const absX = Math.abs(deltaX);
      const absY = Math.abs(deltaY);
      
      let direction = null;
      if (absX > absY) {
        direction = deltaX > 0 ? 'right' : 'left';
      } else {
        direction = deltaY > 0 ? 'down' : 'up';
      }
      
      setTouchData(prev => ({
        ...prev,
        currentX,
        currentY,
        deltaX,
        deltaY,
        direction,
        isSwiping: Math.max(absX, absY) > 10
      }));
    };

    const handleTouchEnd = (e) => {
      const endTime = Date.now();
      const duration = endTime - startTime;
      const distance = Math.sqrt(
        Math.pow(touchData.deltaX, 2) + Math.pow(touchData.deltaY, 2)
      );
      const velocity = distance / duration;
      
      setTouchData(prev => ({
        ...prev,
        velocity,
        isSwiping: false
      }));
    };

    element.addEventListener('touchstart', handleTouchStart, { passive: false });
    element.addEventListener('touchmove', handleTouchMove, { passive: false });
    element.addEventListener('touchend', handleTouchEnd, { passive: false });

    return () => {
      element.removeEventListener('touchstart', handleTouchStart);
      element.removeEventListener('touchmove', handleTouchMove);
      element.removeEventListener('touchend', handleTouchEnd);
    };
  }, [element, touchData.deltaX, touchData.deltaY]);

  return touchData;
};

// Hook for swipe gestures
export const useSwipe = (onSwipe, threshold = 50) => {
  const [touchStart, setTouchStart] = useState(null);
  const [touchEnd, setTouchEnd] = useState(null);

  const minSwipeDistance = threshold;

  const onTouchStart = (e) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    
    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;

    if (isLeftSwipe) {
      onSwipe('left');
    } else if (isRightSwipe) {
      onSwipe('right');
    }
  };

  return {
    onTouchStart,
    onTouchMove,
    onTouchEnd
  };
};
```

### Step 2: Swipeable Component

```jsx
// webui/src/components/SwipeableCard.jsx

import React from 'react';
import { useSwipe } from '../hooks/useTouch';

const SwipeableCard = ({ children, onSwipeLeft, onSwipeRight }) => {
  const { onTouchStart, onTouchMove, onTouchEnd } = useSwipe((direction) => {
    if (direction === 'left' && onSwipeLeft) {
      onSwipeLeft();
    } else if (direction === 'right' && onSwipeRight) {
      onSwipeRight();
    }
  });

  return (
    <div
      className="swipeable-card"
      onTouchStart={onTouchStart}
      onTouchMove={onTouchMove}
      onTouchEnd={onTouchEnd}
      style={{
        touchAction: 'pan-x',
        cursor: 'grab'
      }}
    >
      {children}
    </div>
  );
};

export default SwipeableCard;
```

## Phase 3: Offline Capabilities

### Step 1: Service Worker Setup

```javascript
// webui/public/sw.js

const CACHE_NAME = 'piwardrive-v1';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json',
  '/favicon.ico'
];

// Install service worker
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

// Fetch event with network-first strategy for API calls
self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/api/')) {
    // Network-first strategy for API calls
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // Cache successful API responses
          if (response.status === 200) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME)
              .then((cache) => cache.put(event.request, responseClone));
          }
          return response;
        })
        .catch(() => {
          // Return cached response if network fails
          return caches.match(event.request);
        })
    );
  } else {
    // Cache-first strategy for static assets
    event.respondWith(
      caches.match(event.request)
        .then((response) => {
          if (response) {
            return response;
          }
          return fetch(event.request);
        })
    );
  }
});

// Update service worker
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Background sync for queued requests
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync') {
    event.waitUntil(processQueuedRequests());
  }
});

async function processQueuedRequests() {
  const queue = await getQueuedRequests();
  
  for (const request of queue) {
    try {
      await fetch(request.url, {
        method: request.method,
        headers: request.headers,
        body: request.body
      });
      
      // Remove from queue on success
      await removeFromQueue(request.id);
    } catch (error) {
      console.error('Failed to sync request:', error);
    }
  }
}

async function getQueuedRequests() {
  // Implementation to get queued requests from IndexedDB
  const db = await openDB('PiWardriveQueue', 1);
  const tx = db.transaction('requests', 'readonly');
  const store = tx.objectStore('requests');
  return store.getAll();
}

async function removeFromQueue(requestId) {
  // Implementation to remove request from IndexedDB
  const db = await openDB('PiWardriveQueue', 1);
  const tx = db.transaction('requests', 'readwrite');
  const store = tx.objectStore('requests');
  await store.delete(requestId);
}
```

### Step 2: Offline Data Manager

```javascript
// webui/src/utils/offlineManager.js

class OfflineManager {
  constructor() {
    this.dbName = 'PiWardriveOffline';
    this.version = 1;
    this.db = null;
    this.initDB();
  }

  async initDB() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve(this.db);
      };
      
      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        
        // Create stores
        const scanStore = db.createObjectStore('scans', { keyPath: 'id' });
        const configStore = db.createObjectStore('config', { keyPath: 'key' });
        const queueStore = db.createObjectStore('queue', { keyPath: 'id' });
        
        // Create indexes
        scanStore.createIndex('timestamp', 'timestamp');
        queueStore.createIndex('timestamp', 'timestamp');
      };
    });
  }

  async saveData(storeName, data) {
    if (!this.db) await this.initDB();
    
    const tx = this.db.transaction([storeName], 'readwrite');
    const store = tx.objectStore(storeName);
    
    return new Promise((resolve, reject) => {
      const request = store.put(data);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async getData(storeName, key) {
    if (!this.db) await this.initDB();
    
    const tx = this.db.transaction([storeName], 'readonly');
    const store = tx.objectStore(storeName);
    
    return new Promise((resolve, reject) => {
      const request = store.get(key);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async getAllData(storeName) {
    if (!this.db) await this.initDB();
    
    const tx = this.db.transaction([storeName], 'readonly');
    const store = tx.objectStore(storeName);
    
    return new Promise((resolve, reject) => {
      const request = store.getAll();
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async queueRequest(url, method, data) {
    const request = {
      id: Date.now().toString(),
      url,
      method,
      data,
      timestamp: new Date().toISOString()
    };
    
    await this.saveData('queue', request);
    
    // Try to process immediately if online
    if (navigator.onLine) {
      this.processQueue();
    }
    
    return request.id;
  }

  async processQueue() {
    const queuedRequests = await this.getAllData('queue');
    
    for (const request of queuedRequests) {
      try {
        const response = await fetch(request.url, {
          method: request.method,
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(request.data)
        });
        
        if (response.ok) {
          await this.deleteData('queue', request.id);
        }
      } catch (error) {
        console.error('Failed to process queued request:', error);
      }
    }
  }

  async deleteData(storeName, key) {
    if (!this.db) await this.initDB();
    
    const tx = this.db.transaction([storeName], 'readwrite');
    const store = tx.objectStore(storeName);
    
    return new Promise((resolve, reject) => {
      const request = store.delete(key);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }
}

export const offlineManager = new OfflineManager();
```

## Phase 4: Progressive Web App (PWA) Features

### Step 1: Web App Manifest

```json
{
  "name": "PiWardrive",
  "short_name": "PiWardrive",
  "description": "Professional headless mapping and diagnostic suite",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#007bff",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-152x152.png",
      "sizes": "152x152",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-384x384.png",
      "sizes": "384x384",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "categories": ["productivity", "utilities", "developer"],
  "lang": "en-US",
  "dir": "ltr",
  "scope": "/",
  "prefer_related_applications": false
}
```

### Step 2: PWA Installation Handler

```jsx
// webui/src/components/PWAInstaller.jsx

import React, { useState, useEffect } from 'react';

const PWAInstaller = () => {
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [showInstallPrompt, setShowInstallPrompt] = useState(false);
  const [isInstalled, setIsInstalled] = useState(false);

  useEffect(() => {
    const handleBeforeInstallPrompt = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setShowInstallPrompt(true);
    };

    const handleAppInstalled = () => {
      setIsInstalled(true);
      setShowInstallPrompt(false);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    window.addEventListener('appinstalled', handleAppInstalled);

    // Check if app is already installed
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true);
    }

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, []);

  const handleInstallClick = async () => {
    if (!deferredPrompt) return;

    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    
    if (outcome === 'accepted') {
      setIsInstalled(true);
    }
    
    setDeferredPrompt(null);
    setShowInstallPrompt(false);
  };

  if (isInstalled || !showInstallPrompt) {
    return null;
  }

  return (
    <div className="pwa-installer">
      <div className="pwa-installer-content">
        <h3>Install PiWardrive</h3>
        <p>Install PiWardrive on your device for the best experience</p>
        <div className="pwa-installer-actions">
          <button onClick={handleInstallClick} className="btn btn-primary">
            Install
          </button>
          <button 
            onClick={() => setShowInstallPrompt(false)} 
            className="btn btn-secondary"
          >
            Maybe Later
          </button>
        </div>
      </div>
    </div>
  );
};

export default PWAInstaller;
```

### Step 3: Offline Status Indicator

```jsx
// webui/src/components/OfflineIndicator.jsx

import React, { useState, useEffect } from 'react';

const OfflineIndicator = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [queueSize, setQueueSize] = useState(0);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  useEffect(() => {
    const updateQueueSize = async () => {
      try {
        const { offlineManager } = await import('../utils/offlineManager');
        const queue = await offlineManager.getAllData('queue');
        setQueueSize(queue.length);
      } catch (error) {
        console.error('Failed to get queue size:', error);
      }
    };

    updateQueueSize();
    const interval = setInterval(updateQueueSize, 5000);

    return () => clearInterval(interval);
  }, []);

  if (isOnline && queueSize === 0) {
    return null;
  }

  return (
    <div className={`offline-indicator ${isOnline ? 'online' : 'offline'}`}>
      <div className="offline-indicator-content">
        <span className="offline-indicator-icon">
          {isOnline ? '🟢' : '🔴'}
        </span>
        <span className="offline-indicator-text">
          {isOnline ? 'Online' : 'Offline'}
        </span>
        {queueSize > 0 && (
          <span className="offline-indicator-queue">
            ({queueSize} queued)
          </span>
        )}
      </div>
    </div>
  );
};

export default OfflineIndicator;
```

## Phase 5: Mobile Map Optimization

### Step 1: Touch-Friendly Map Controls

```jsx
// webui/src/components/MobileMapControls.jsx

import React, { useState } from 'react';

const MobileMapControls = ({ onZoomIn, onZoomOut, onCenter, onToggleLayer }) => {
  const [showLayerMenu, setShowLayerMenu] = useState(false);

  const layers = [
    { id: 'wifi', name: 'WiFi Networks', icon: '📶' },
    { id: 'bluetooth', name: 'Bluetooth Devices', icon: '🔵' },
    { id: 'cellular', name: 'Cellular Towers', icon: '📡' },
    { id: 'heat', name: 'Heat Map', icon: '🔥' }
  ];

  return (
    <div className="mobile-map-controls">
      <div className="map-control-group">
        <button className="map-control-btn" onClick={onZoomIn}>
          <span>+</span>
        </button>
        <button className="map-control-btn" onClick={onZoomOut}>
          <span>-</span>
        </button>
        <button className="map-control-btn" onClick={onCenter}>
          <span>🎯</span>
        </button>
      </div>
      
      <div className="map-layer-control">
        <button 
          className="map-control-btn layer-btn"
          onClick={() => setShowLayerMenu(!showLayerMenu)}
        >
          <span>🗂️</span>
        </button>
        
        {showLayerMenu && (
          <div className="layer-menu">
            {layers.map(layer => (
              <button
                key={layer.id}
                className="layer-menu-item"
                onClick={() => onToggleLayer(layer.id)}
              >
                <span className="layer-icon">{layer.icon}</span>
                <span className="layer-name">{layer.name}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default MobileMapControls;
```

### Step 2: Performance Monitoring Component

```jsx
// webui/src/components/MobilePerformanceMonitor.jsx

import React, { useState, useEffect } from 'react';

const MobilePerformanceMonitor = () => {
  const [performance, setPerformance] = useState({
    battery: null,
    memory: null,
    connection: null,
    location: null
  });

  useEffect(() => {
    const updatePerformance = async () => {
      const newPerformance = { ...performance };

      // Battery API
      if ('getBattery' in navigator) {
        try {
          const battery = await navigator.getBattery();
          newPerformance.battery = {
            level: Math.round(battery.level * 100),
            charging: battery.charging
          };
        } catch (error) {
          console.error('Battery API not supported');
        }
      }

      // Memory API
      if ('memory' in performance) {
        newPerformance.memory = {
          used: Math.round(performance.memory.usedJSHeapSize / 1024 / 1024),
          total: Math.round(performance.memory.totalJSHeapSize / 1024 / 1024),
          limit: Math.round(performance.memory.jsHeapSizeLimit / 1024 / 1024)
        };
      }

      // Connection API
      if ('connection' in navigator) {
        newPerformance.connection = {
          effectiveType: navigator.connection.effectiveType,
          downlink: navigator.connection.downlink,
          rtt: navigator.connection.rtt
        };
      }

      // Geolocation
      if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            newPerformance.location = {
              accuracy: position.coords.accuracy,
              timestamp: new Date(position.timestamp).toLocaleTimeString()
            };
            setPerformance(newPerformance);
          },
          (error) => {
            console.error('Geolocation error:', error);
          },
          { timeout: 5000 }
        );
      }

      setPerformance(newPerformance);
    };

    updatePerformance();
    const interval = setInterval(updatePerformance, 30000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="mobile-performance-monitor">
      <div className="performance-grid">
        {performance.battery && (
          <div className="performance-item">
            <div className="performance-icon">
              {performance.battery.charging ? '🔌' : '🔋'}
            </div>
            <div className="performance-value">
              {performance.battery.level}%
            </div>
          </div>
        )}
        
        {performance.memory && (
          <div className="performance-item">
            <div className="performance-icon">💾</div>
            <div className="performance-value">
              {performance.memory.used}MB
            </div>
          </div>
        )}
        
        {performance.connection && (
          <div className="performance-item">
            <div className="performance-icon">📶</div>
            <div className="performance-value">
              {performance.connection.effectiveType}
            </div>
          </div>
        )}
        
        {performance.location && (
          <div className="performance-item">
            <div className="performance-icon">📍</div>
            <div className="performance-value">
              ±{Math.round(performance.location.accuracy)}m
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MobilePerformanceMonitor;
```

## Phase 6: Testing and Optimization

### Step 1: Mobile Testing Framework

```javascript
// webui/src/tests/mobileTests.js

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import userEvent from '@testing-library/user-event';

// Mock touch events
const mockTouchEvent = (type, touches) => {
  const event = new Event(type, { bubbles: true });
  event.touches = touches;
  event.targetTouches = touches;
  return event;
};

describe('Mobile Interface Tests', () => {
  test('should render mobile navigation', () => {
    render(<MobileLayout />);
    expect(screen.getByRole('navigation')).toBeInTheDocument();
  });

  test('should handle swipe gestures', async () => {
    const onSwipe = jest.fn();
    render(<SwipeableCard onSwipeLeft={onSwipe} />);
    
    const card = screen.getByTestId('swipeable-card');
    
    // Simulate swipe left
    fireEvent(card, mockTouchEvent('touchstart', [{ clientX: 100, clientY: 100 }]));
    fireEvent(card, mockTouchEvent('touchmove', [{ clientX: 50, clientY: 100 }]));
    fireEvent(card, mockTouchEvent('touchend', []));
    
    await waitFor(() => {
      expect(onSwipe).toHaveBeenCalledWith('left');
    });
  });

  test('should handle touch-friendly button taps', async () => {
    const onClick = jest.fn();
    render(<button onClick={onClick}>Test Button</button>);
    
    const button = screen.getByRole('button');
    
    // Simulate touch tap
    fireEvent(button, mockTouchEvent('touchstart', [{ clientX: 100, clientY: 100 }]));
    fireEvent(button, mockTouchEvent('touchend', []));
    
    await waitFor(() => {
      expect(onClick).toHaveBeenCalled();
    });
  });

  test('should be responsive to different screen sizes', () => {
    // Test mobile breakpoint
    global.innerWidth = 480;
    global.dispatchEvent(new Event('resize'));
    
    render(<MobileLayout />);
    expect(screen.getByTestId('mobile-nav')).toBeVisible();
    
    // Test desktop breakpoint
    global.innerWidth = 1024;
    global.dispatchEvent(new Event('resize'));
    
    expect(screen.queryByTestId('mobile-nav')).not.toBeInTheDocument();
  });
});
```

### Step 2: Performance Testing

```javascript
// webui/src/tests/performanceTests.js

describe('Mobile Performance Tests', () => {
  test('should load page within 3 seconds', async () => {
    const startTime = performance.now();
    
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByTestId('main-content')).toBeInTheDocument();
    });
    
    const loadTime = performance.now() - startTime;
    expect(loadTime).toBeLessThan(3000);
  });

  test('should handle offline state', async () => {
    // Mock offline state
    Object.defineProperty(navigator, 'onLine', {
      writable: true,
      value: false
    });
    
    render(<OfflineIndicator />);
    
    expect(screen.getByText('Offline')).toBeInTheDocument();
  });

  test('should cache data for offline use', async () => {
    const testData = { id: 1, name: 'Test' };
    
    await offlineManager.saveData('test', testData);
    const cachedData = await offlineManager.getData('test', 1);
    
    expect(cachedData).toEqual(testData);
  });
});
```

This comprehensive mobile optimization implementation provides:

1. **Responsive Design Foundation**: Mobile-first CSS framework with touch-friendly controls
2. **Touch-Friendly Interface**: Gesture handling, swipe support, and touch optimizations
3. **Offline Capabilities**: Service worker, data caching, and background sync
4. **Progressive Web App Features**: App manifest, installation prompts, and native-like experience
5. **Mobile Map Optimization**: Touch controls and performance monitoring
6. **Testing Framework**: Comprehensive mobile testing and performance validation

The implementation ensures that PiWardrive provides an excellent mobile experience for field operations while maintaining full functionality across all device types.
