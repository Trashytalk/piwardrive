import React from 'react';
import ReactDOM from 'react-dom/client';
import { install } from './exceptionHandler.js';
import './auth.js';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import App from './App.jsx';
import ConsoleView from './components/ConsoleView.jsx';
import SplitScreen from './components/SplitScreen.jsx';
import MobileLayout from './components/MobileLayout.jsx';
import { initMobileFeatures } from './mobileFeatures.js';
import ErrorBoundary from './components/ErrorBoundary.jsx';

let Root = App;
const path = window.location.pathname;
if (path.startsWith('/console')) Root = ConsoleView;
if (path.startsWith('/split')) Root = SplitScreen;
import SettingsForm from './components/SettingsForm.jsx';
import SplitView from './components/SplitView.jsx';
import NavBar from './components/NavBar.jsx';
import HealthImport from './components/HealthImport.jsx';

install();
initMobileFeatures();

const origFetch = window.fetch;
window.fetch = (url, opts = {}) => {
  const token = localStorage.getItem('token');
  if (token) {
    opts = {
      ...opts,
      headers: { ...(opts.headers || {}), Authorization: `Bearer ${token}` },
    };
  }
  return origFetch(url, opts);
};

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ErrorBoundary>
      <BrowserRouter>
        <NavBar />
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/console" element={<ConsoleView />} />
          <Route path="/settings" element={<SettingsForm />} />
          <Route path="/import-health" element={<HealthImport />} />
          <Route path="/split" element={<SplitView />} />
          <Route path="/mobile/*" element={<MobileLayout />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  </React.StrictMode>
);
