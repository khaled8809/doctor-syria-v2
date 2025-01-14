import React from 'react';
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  useTheme,
  Divider,
} from '@mui/material';
import {
  ChevronLeft,
  Dashboard,
  People,
  CalendarToday,
  LocalHospital,
  Assignment,
  Business,
  Group,
  Analytics,
  Message,
  Settings,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../../hooks/useAuth';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const theme = useTheme();
  const navigate = useNavigate();
  const { user } = useAuth();

  const menuItems = [
    { text: 'Dashboard', icon: <Dashboard />, path: '/dashboard' },
    { text: 'Patients', icon: <People />, path: '/patients' },
    { text: 'Schedule', icon: <CalendarToday />, path: '/schedule' },
    { text: 'Medical Records', icon: <LocalHospital />, path: '/medical-records' },
    { text: 'Prescriptions', icon: <Assignment />, path: '/prescriptions' },
    { text: 'Hospitals', icon: <Business />, path: '/hospitals' },
    { text: 'Staff', icon: <Group />, path: '/staff' },
    { text: 'Analytics', icon: <Analytics />, path: '/analytics' },
    { text: 'Messages', icon: <Message />, path: '/messages' },
    { text: 'Settings', icon: <Settings />, path: '/settings' },
  ];

  const handleNavigate = (path: string) => {
    navigate(path);
    onClose();
  };

  return (
    <Drawer
      variant="persistent"
      anchor="right"
      open={isOpen}
      sx={{
        width: 240,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: 240,
          boxSizing: 'border-box',
          backgroundColor: theme.palette.background.default,
        },
      }}
    >
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          padding: theme.spacing(0, 1),
          ...theme.mixins.toolbar,
          justifyContent: 'flex-start',
        }}
      >
        <IconButton onClick={onClose}>
          <ChevronLeft />
        </IconButton>
      </Box>
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem
            button
            key={item.text}
            onClick={() => handleNavigate(item.path)}
            sx={{
              '&:hover': {
                backgroundColor: theme.palette.action.hover,
              },
            }}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar;
