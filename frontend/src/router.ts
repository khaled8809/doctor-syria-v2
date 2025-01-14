import { createBrowserRouter } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import AuthLayout from './layouts/AuthLayout';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import ForgotPassword from './pages/auth/ForgotPassword';
import Dashboard from './pages/Dashboard';
import Patients from './pages/Patients';
import Profile from './pages/Profile';
import Settings from './pages/Settings';
import Schedule from './pages/Schedule';
import MedicalRecords from './pages/MedicalRecords';
import Prescriptions from './pages/Prescriptions';
import Hospitals from './pages/Hospitals';
import Departments from './pages/Departments';
import Staff from './pages/Staff';
import Analytics from './pages/Analytics';
import Messages from './pages/Messages';
import NotFound from './pages/NotFound';

const router = createBrowserRouter(
  [
    {
      path: '/',
      element: <MainLayout />,
      children: [
        { path: '/', element: <Dashboard /> },
        { path: '/patients', element: <Patients /> },
        { path: '/schedule', element: <Schedule /> },
        { path: '/medical-records', element: <MedicalRecords /> },
        { path: '/prescriptions', element: <Prescriptions /> },
        { path: '/hospitals', element: <Hospitals /> },
        { path: '/departments', element: <Departments /> },
        { path: '/staff', element: <Staff /> },
        { path: '/analytics', element: <Analytics /> },
        { path: '/messages', element: <Messages /> },
        { path: '/profile', element: <Profile /> },
        { path: '/settings', element: <Settings /> },
      ],
    },
    {
      path: '/auth',
      element: <AuthLayout />,
      children: [
        { path: 'login', element: <Login /> },
        { path: 'register', element: <Register /> },
        { path: 'forgot-password', element: <ForgotPassword /> },
      ],
    },
    {
      path: '*',
      element: <NotFound />,
    },
  ],
  {
    basename: '/doctor-syria-v2',
  }
);

export default router;
