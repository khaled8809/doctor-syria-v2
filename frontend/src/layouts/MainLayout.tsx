import React from 'react';
import { Box, Container } from '@mui/material';
import { Outlet } from 'react-router-dom';
import Navbar from '../components/Layout/Navbar';
import Sidebar from '../components/Layout/Sidebar';
import { useSettings } from '../contexts/SettingsContext';

const MainLayout: React.FC = () => {
  const { settings } = useSettings();

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', direction: settings.direction }}>
      <Navbar />
      <Sidebar />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          py: 8,
          px: 2,
          bgcolor: 'background.default'
        }}
      >
        <Container maxWidth="xl">
          <Box sx={{ mt: 8 }}>
            <Outlet />
          </Box>
        </Container>
      </Box>
    </Box>
  );
};

export default MainLayout;
