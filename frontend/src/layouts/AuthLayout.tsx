import React from 'react';
import { Box, Container } from '@mui/material';
import { Outlet } from 'react-router-dom';
import { useSettings } from '../contexts/SettingsContext';

const AuthLayout: React.FC = () => {
  const { settings } = useSettings();

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        direction: settings.direction,
        bgcolor: 'background.default'
      }}
    >
      <Container
        maxWidth="sm"
        sx={{
          py: {
            xs: '80px',
            md: '120px'
          },
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        <Box
          sx={{
            width: '100%',
            maxWidth: 480,
            bgcolor: 'background.paper',
            borderRadius: 2,
            p: 4,
            boxShadow: (theme) => theme.shadows[20]
          }}
        >
          <Outlet />
        </Box>
      </Container>
    </Box>
  );
};

export default AuthLayout;
