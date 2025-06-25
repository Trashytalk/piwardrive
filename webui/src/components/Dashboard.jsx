import { useEffect, useState } from 'react';
import BatteryStatus from './BatteryStatus.jsx';
import ServiceStatus from './ServiceStatus.jsx';
import HandshakeCount from './HandshakeCount.jsx';
import SignalStrength from './SignalStrength.jsx';
import NetworkThroughput from './NetworkThroughput.jsx';
import CPUTempGraph from './CPUTempGraph.jsx';
import StatsDashboard from './StatsDashboard.jsx';
import VehicleStats from './VehicleStats.jsx';
import Orientation from './Orientation.jsx';
import VehicleInfo from './VehicleInfo.jsx';

const COMPONENTS = {
  BatteryStatusWidget: BatteryStatus,
  ServiceStatusWidget: ServiceStatus,
  HandshakeCounterWidget: HandshakeCount,
  SignalStrengthWidget: SignalStrength,
  NetworkThroughputWidget: NetworkThroughput,
  CPUTempGraphWidget: CPUTempGraph,
  OrientationWidget: Orientation,
  VehicleSpeedWidget: VehicleStats,
  VehicleInfoWidget: VehicleInfo,
  StatsDashboard: StatsDashboard,
};

export default function Dashboard({ metrics }) {
  const [names, setNames] = useState([]);

  useEffect(() => {
    async function load() {
      try {
        const resp = await fetch('/dashboard-settings');
        const data = await resp.json();
        if (data.widgets && data.widgets.length) {
          setNames(data.widgets);
          return;
        }
      } catch (_) {}
      try {
        const resp = await fetch('/api/widgets');
        const data = await resp.json();
        setNames(data.widgets || []);
      } catch (_) {}
    }
    load();
  }, []);

  return (
    <div>
      {names.map((name) => {
        const Comp = COMPONENTS[name];
        if (Comp) return <Comp key={name} metrics={metrics} />;
        return <div key={name}>Unknown widget: {name}</div>;
      })}
    </div>
  );
}
