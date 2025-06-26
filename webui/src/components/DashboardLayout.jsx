import { useEffect, useState } from 'react';
import BatteryStatus from './BatteryStatus.jsx';
import ServiceStatus from './ServiceStatus.jsx';
import HandshakeCount from './HandshakeCount.jsx';
import SignalStrength from './SignalStrength.jsx';
import NetworkThroughput from './NetworkThroughput.jsx';
import CPUTempGraph from './CPUTempGraph.jsx';
import GPSStatus from './GPSStatus.jsx';
import StorageUsage from './StorageUsage.jsx';
import DiskUsageTrend from './DiskUsageTrend.jsx';
import VehicleSpeed from './VehicleSpeed.jsx';
import DBStats from './DBStats.jsx';
import HealthStatus from './HealthStatus.jsx';
import HealthAnalysis from './HealthAnalysis.jsx';
import LoRaScan from './LoRaScan.jsx';
import LogViewer from './LogViewer.jsx';

const COMPONENTS = {
  BatteryStatusWidget: BatteryStatus,
  ServiceStatusWidget: ServiceStatus,
  HandshakeCounterWidget: HandshakeCount,
  SignalStrengthWidget: SignalStrength,
  NetworkThroughputWidget: NetworkThroughput,
  CPUTempGraphWidget: CPUTempGraph,
  GPSStatusWidget: GPSStatus,
  StorageUsageWidget: StorageUsage,
  DiskUsageTrendWidget: DiskUsageTrend,
  VehicleSpeedWidget: VehicleSpeed,
  DBStatsWidget: DBStats,
  HealthStatusWidget: HealthStatus,
  HealthAnalysisWidget: HealthAnalysis,
  LoRaScanWidget: LoRaScan,
  LogViewer: LogViewer,
};

export default function DashboardLayout({ metrics }) {
  const [order, setOrder] = useState([]);

  useEffect(() => {
    fetch('/dashboard-settings')
      .then(r => r.json())
      .then(d => {
        if (d.layout && d.layout.length > 0) {
          setOrder(d.layout.map(w => w.cls));
        } else if (d.widgets) {
          setOrder(d.widgets);
        }
      });
  }, []);

  const save = (items) => {
    setOrder(items);
    const layout = items.map(cls => ({ cls }));
    fetch('/dashboard-settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ layout }),
    }).catch(() => {});
  };

  const onDragStart = (e, idx) => {
    e.dataTransfer.setData('text/plain', String(idx));
  };

  const onDrop = (e, idx) => {
    e.preventDefault();
    const from = parseInt(e.dataTransfer.getData('text/plain'), 10);
    if (Number.isNaN(from) || from === idx) return;
    const items = [...order];
    const [moved] = items.splice(from, 1);
    items.splice(idx, 0, moved);
    save(items);
  };

  const onDragOver = (e) => e.preventDefault();

  return (
    <div>
      {order.map((name, idx) => {
        const Comp = COMPONENTS[name];
        return (
          <div
            key={name}
            draggable
            onDragStart={e => onDragStart(e, idx)}
            onDrop={e => onDrop(e, idx)}
            onDragOver={onDragOver}
            style={{ border: '1px solid #ccc', padding: '4px', marginBottom: '4px' }}
          >
            {Comp ? <Comp metrics={metrics} /> : <div>{name}</div>}
          </div>
        );
      })}
    </div>
  );
}
