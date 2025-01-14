import React from 'react';
import { Box, CssBaseline, ThemeProvider } from '@mui/material';
import { useTheme } from '../../../hooks/useTheme';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import NotificationSystem from './NotificationSystem';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  const { theme, toggleTheme } = useTheme();
  const [sidebarOpen, setSidebarOpen] = React.useState(true);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', direction: 'rtl' }}>
        <TopBar
          onSidebarToggle={toggleSidebar}
          onThemeToggle={toggleTheme}
        />
        <Sidebar
          open={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
        />
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3,
            width: { sm: `calc(100% - ${240}px)` },
            mt: 8
          }}
        >
          {children}
        </Box>
        <NotificationSystem />
      </Box>
    </ThemeProvider>
  );
};

export default DashboardLayout;
