import React, { Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import LoadingOverlay from './components/common/LoadingOverlay';

// Lazy loaded components
const Landing = React.lazy(() => import('./pages/Landing'));
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const Schedule = React.lazy(() => import('./pages/Schedule'));
const Patients = React.lazy(() => import('./pages/Patients'));
const Inventory = React.lazy(() => import('./pages/Inventory'));
const Reports = React.lazy(() => import('./pages/Reports'));
const Settings = React.lazy(() => import('./pages/Settings'));
const Profile = React.lazy(() => import('./pages/Profile'));
const Login = React.lazy(() => import('./pages/auth/Login'));
const Register = React.lazy(() => import('./pages/auth/Register'));
const ForgotPassword = React.lazy(() => import('./pages/auth/ForgotPassword'));
const ResetPassword = React.lazy(() => import('./pages/auth/ResetPassword'));

const AppRouter: React.FC = () => {
  return (
    <Suspense fallback={<LoadingOverlay />}>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/schedule" element={<Schedule />} />
        <Route path="/patients" element={<Patients />} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Suspense>
  );
};

export default AppRouter;
