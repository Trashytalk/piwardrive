import { useEffect, useRef, useState } from 'react';
import { Link, Routes, Route, Navigate } from 'react-router-dom';
import MobileMap from './MobileMap.jsx';
import MobileAlerts from './MobileAlerts.jsx';
import DashboardLayout from './DashboardLayout.jsx';

export default function MobileLayout() {
  const [navOpen, setNavOpen] = useState(false);
  const containerRef = useRef(null);

  const toggleNav = () => setNavOpen((o) => !o);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return undefined;
    let startX = null;
    const onStart = (e) => {
      startX = e.touches[0].clientX;
    };
    const onEnd = (e) => {
      if (startX == null) return;
      const dist = e.changedTouches[0].clientX - startX;
      if (dist > 60) setNavOpen(true);
      if (dist < -60) setNavOpen(false);
      startX = null;
    };
    el.addEventListener('touchstart', onStart);
    el.addEventListener('touchend', onEnd);
    return () => {
      el.removeEventListener('touchstart', onStart);
      el.removeEventListener('touchend', onEnd);
    };
  }, []);

  const navStyle = {
    display: navOpen ? 'block' : 'none',
    background: '#333',
    color: '#fff',
    padding: '0.5em',
  };

  const btnStyle = {
    fontSize: '1.5em',
    padding: '0.2em 0.5em',
    background: 'transparent',
    border: 'none',
    color: '#333',
  };

  const tableStyle = {
    width: '100%',
    borderCollapse: 'collapse',
  };

  return (
    <div ref={containerRef}>
      <button onClick={toggleNav} style={btnStyle}>
        ☰
      </button>
      <nav style={navStyle} onClick={() => setNavOpen(false)}>
        <Link to="/mobile/map" style={{ marginRight: '1em', color: '#fff' }}>
          Map
        </Link>
        <Link
          to="/mobile/dashboard"
          style={{ marginRight: '1em', color: '#fff' }}
        >
          Dashboard
        </Link>
        <Link to="/mobile/alerts" style={{ color: '#fff' }}>
          Alerts
        </Link>
      </nav>
      <div style={{ padding: '0.5em' }}>
        <Routes>
          <Route path="map" element={<MobileMap />} />
          <Route
            path="dashboard"
            element={<DashboardLayout tableStyle={tableStyle} />}
          />
          <Route path="alerts" element={<MobileAlerts />} />
          <Route path="*" element={<Navigate to="map" replace />} />
        </Routes>
      </div>
    </div>
  );
}
