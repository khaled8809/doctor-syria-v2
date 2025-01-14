import React, { Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import LoadingSpinner from '../components/common/LoadingSpinner';

// Lazy loaded components
const Dashboard = React.lazy(() => import('../pages/Dashboard'));
const Patients = React.lazy(() => import('../pages/Patients'));
const Appointments = React.lazy(() => import('../pages/Appointments'));
const Profile = React.lazy(() => import('../pages/Profile'));
const Settings = React.lazy(() => import('../pages/Settings'));
const Reports = React.lazy(() => import('../pages/Reports'));

// Layout components
const MainLayout = React.lazy(() => import('../layouts/MainLayout'));
const AuthLayout = React.lazy(() => import('../layouts/AuthLayout'));

// Auth pages
const Login = React.lazy(() => import('../pages/auth/Login'));
const Register = React.lazy(() => import('../pages/auth/Register'));
const ForgotPassword = React.lazy(() => import('../pages/auth/ForgotPassword'));

const LoadingFallback = () => (
  <div className="flex items-center justify-center min-h-screen">
    <LoadingSpinner size="large" />
  </div>
);

const AppRoutes = () => {
  return (
    <Suspense fallback={<LoadingFallback />}>
      <Routes>
        {/* Auth Routes */}
        <Route element={
          <Suspense fallback={<LoadingFallback />}>
            <AuthLayout />
          </Suspense>
        }>
          <Route path="/login" element={
            <Suspense fallback={<LoadingFallback />}>
              <Login />
            </Suspense>
          } />
          <Route path="/register" element={
            <Suspense fallback={<LoadingFallback />}>
              <Register />
            </Suspense>
          } />
          <Route path="/forgot-password" element={
            <Suspense fallback={<LoadingFallback />}>
              <ForgotPassword />
            </Suspense>
          } />
        </Route>

        {/* Main App Routes */}
        <Route element={
          <Suspense fallback={<LoadingFallback />}>
            <MainLayout />
          </Suspense>
        }>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={
            <Suspense fallback={<LoadingFallback />}>
              <Dashboard />
            </Suspense>
          } />
          <Route path="/patients/*" element={
            <Suspense fallback={<LoadingFallback />}>
              <Patients />
            </Suspense>
          } />
          <Route path="/appointments/*" element={
            <Suspense fallback={<LoadingFallback />}>
              <Appointments />
            </Suspense>
          } />
          <Route path="/profile" element={
            <Suspense fallback={<LoadingFallback />}>
              <Profile />
            </Suspense>
          } />
          <Route path="/settings" element={
            <Suspense fallback={<LoadingFallback />}>
              <Settings />
            </Suspense>
          } />
          <Route path="/reports/*" element={
            <Suspense fallback={<LoadingFallback />}>
              <Reports />
            </Suspense>
          } />
        </Route>

        {/* 404 Route */}
        <Route path="*" element={<Navigate to="/404" replace />} />
      </Routes>
    </Suspense>
  );
};

export default AppRoutes;
