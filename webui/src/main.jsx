import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import ConsoleView from './components/ConsoleView.jsx';
import SplitScreen from './components/SplitScreen.jsx';

let Root = App;
const path = window.location.pathname;
if (path.startsWith('/console')) Root = ConsoleView;
if (path.startsWith('/split')) Root = SplitScreen;

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Root />
  </React.StrictMode>
);
