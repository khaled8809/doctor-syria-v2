import React, { Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoadingOverlay from './components/common/LoadingOverlay';

// Lazy loaded components
const Landing = React.lazy(() => import('./pages/Landing'));
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const Patients = React.lazy(() => import('./pages/Patients'));
const PatientDetails = React.lazy(() => import('./pages/PatientDetails'));
const Schedule = React.lazy(() => import('./pages/Schedule'));
const Reports = React.lazy(() => import('./pages/Reports'));
const Settings = React.lazy(() => import('./pages/Settings'));
const NotFound = React.lazy(() => import('./pages/NotFound'));
const Messages = React.lazy(() => import('./pages/Messages'));
const Profile = React.lazy(() => import('./pages/Profile'));
const MedicalRecords = React.lazy(() => import('./pages/MedicalRecords'));
const Hospitals = React.lazy(() => import('./pages/Hospitals'));
const Staff = React.lazy(() => import('./pages/Staff'));
const Resources = React.lazy(() => import('./pages/Resources'));

const AppRouter: React.FC = () => {
  return (
    <BrowserRouter>
      <Suspense fallback={<LoadingOverlay open={true} />}>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/dashboard/*" element={<Dashboard />} />
          <Route path="/patients" element={<Patients />} />
          <Route path="/patients/:id" element={<PatientDetails />} />
          <Route path="/schedule" element={<Schedule />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/messages" element={<Messages />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/medical-records" element={<MedicalRecords />} />
          <Route path="/hospitals" element={<Hospitals />} />
          <Route path="/staff" element={<Staff />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/404" element={<NotFound />} />
          <Route path="*" element={<Navigate to="/404" replace />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
};

export default AppRouter;
