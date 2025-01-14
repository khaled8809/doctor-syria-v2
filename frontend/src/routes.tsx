import { Routes as RouterRoutes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Devices from './pages/Devices';
import Reports from './pages/Reports';
import Resources from './pages/Resources';
import AIModels from './pages/AIModels';
import Schedule from './pages/Schedule';
import Communication from './pages/Communication';
import Settings from './pages/Settings';

export default function Routes() {
  return (
    <RouterRoutes>
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/devices" element={<Devices />} />
      <Route path="/reports" element={<Reports />} />
      <Route path="/resources" element={<Resources />} />
      <Route path="/ai-models" element={<AIModels />} />
      <Route path="/schedule" element={<Schedule />} />
      <Route path="/communication" element={<Communication />} />
      <Route path="/settings" element={<Settings />} />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
    </RouterRoutes>
  );
}
