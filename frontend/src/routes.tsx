import { Navigate, useRoutes } from 'react-router-dom';
import { lazy } from 'react';
import MainLayout from './layouts/MainLayout';
import AuthLayout from './layouts/AuthLayout';
import LoadingScreen from './components/common/LoadingScreen';

const Loadable = (Component: React.ComponentType) => (props: any) => {
  return (
    <React.Suspense fallback={<LoadingScreen />}>
      <Component {...props} />
    </React.Suspense>
  );
};

// Auth
const Login = Loadable(lazy(() => import('./pages/auth/Login')));
const Register = Loadable(lazy(() => import('./pages/auth/Register')));
const ForgotPassword = Loadable(lazy(() => import('./pages/auth/ForgotPassword')));

// Dashboard
const Dashboard = Loadable(lazy(() => import('./pages/Dashboard')));
const Profile = Loadable(lazy(() => import('./pages/Profile')));
const Settings = Loadable(lazy(() => import('./pages/Settings')));

// Medical
const Appointments = Loadable(lazy(() => import('./pages/Schedule')));
const Patients = Loadable(lazy(() => import('./pages/Patients')));
const MedicalRecords = Loadable(lazy(() => import('./pages/MedicalRecords')));
const Prescriptions = Loadable(lazy(() => import('./pages/Prescriptions')));

// Hospital
const Hospitals = Loadable(lazy(() => import('./pages/Hospitals')));
const Departments = Loadable(lazy(() => import('./pages/Departments')));
const Staff = Loadable(lazy(() => import('./pages/Staff')));

// AI & Analytics
const AIModels = Loadable(lazy(() => import('./pages/AIModels')));
const Analytics = Loadable(lazy(() => import('./pages/Analytics')));

// Other
const Messages = Loadable(lazy(() => import('./pages/Messages')));
const NotFound = Loadable(lazy(() => import('./pages/NotFound')));

export default function Router() {
  return useRoutes([
    {
      path: 'auth',
      element: <AuthLayout />,
      children: [
        { path: 'login', element: <Login /> },
        { path: 'register', element: <Register /> },
        { path: 'forgot-password', element: <ForgotPassword /> }
      ]
    },
    {
      path: '/',
      element: <MainLayout />,
      children: [
        { path: '', element: <Navigate to="/dashboard" /> },
        { path: 'dashboard', element: <Dashboard /> },
        { path: 'profile', element: <Profile /> },
        { path: 'settings', element: <Settings /> },
        {
          path: 'appointments',
          children: [
            { path: '', element: <Appointments /> },
            { path: ':id', element: <Appointments /> }
          ]
        },
        {
          path: 'patients',
          children: [
            { path: '', element: <Patients /> },
            { path: ':id', element: <Patients /> }
          ]
        },
        {
          path: 'medical-records',
          children: [
            { path: '', element: <MedicalRecords /> },
            { path: ':id', element: <MedicalRecords /> }
          ]
        },
        {
          path: 'prescriptions',
          children: [
            { path: '', element: <Prescriptions /> },
            { path: ':id', element: <Prescriptions /> }
          ]
        },
        {
          path: 'hospitals',
          children: [
            { path: '', element: <Hospitals /> },
            { path: ':id', element: <Hospitals /> }
          ]
        },
        {
          path: 'departments',
          children: [
            { path: '', element: <Departments /> },
            { path: ':id', element: <Departments /> }
          ]
        },
        {
          path: 'staff',
          children: [
            { path: '', element: <Staff /> },
            { path: ':id', element: <Staff /> }
          ]
        },
        {
          path: 'ai-models',
          children: [
            { path: '', element: <AIModels /> },
            { path: ':id', element: <AIModels /> }
          ]
        },
        { path: 'analytics', element: <Analytics /> },
        { path: 'messages', element: <Messages /> },
        { path: '404', element: <NotFound /> },
        { path: '*', element: <Navigate to="/404" /> }
      ]
    },
    { path: '*', element: <Navigate to="/404" replace /> }
  ]);
}
