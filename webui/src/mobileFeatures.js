export function initMobileFeatures() {
  if ('ondeviceorientation' in window) {
    window.addEventListener('deviceorientation', (e) => {
      const angle = e.alpha != null ? Math.round(e.alpha) : null;
      if (angle != null)
        localStorage.setItem('orientationAngle', String(angle));
    });
  }

  if (navigator.getBattery) {
    navigator.getBattery().then((batt) => {
      const update = () => {
        if (batt.level < 0.15) {
          document.body.dataset.lowBattery = '1';
        } else {
          delete document.body.dataset.lowBattery;
        }
      };
      update();
      batt.addEventListener('levelchange', update);
    });
  }

  if (navigator.connection && navigator.connection.addEventListener) {
    const updateNet = () => {
      localStorage.setItem(
        'connectionType',
        navigator.connection.effectiveType
      );
    };
    navigator.connection.addEventListener('change', updateNet);
    updateNet();
  }

  window.addEventListener('keydown', (e) => {
    if (e.key === 'm') window.location.href = '/mobile/map';
  });
}
