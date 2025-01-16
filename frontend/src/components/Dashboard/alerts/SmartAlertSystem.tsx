import React from 'react';
import {
  Box,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  IconButton
} from '@mui/material';
import {
  Warning,
  Error,
  Info,
  CheckCircle
} from '@mui/icons-material';
import { Notification } from '../../../types/common';

interface SmartAlertSystemProps {
  alerts: Notification[];
  onAlertAction: (alertId: string, action: string) => void;
}

export const SmartAlertSystem: React.FC<SmartAlertSystemProps> = ({ alerts, onAlertAction }) => {
  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'error':
        return <Error color="error" />;
      case 'warning':
        return <Warning color="warning" />;
      case 'success':
        return <CheckCircle color="success" />;
      default:
        return <Info color="info" />;
    }
  };

  const getAlertColor = (type: string) => {
    switch (type) {
      case 'error':
        return 'error';
      case 'warning':
        return 'warning';
      case 'success':
        return 'success';
      default:
        return 'info';
    }
  };

  return (
    <Paper sx={{ p: 2, height: '100%' }}>
      <Typography variant="h6" gutterBottom>
        Alert System
      </Typography>

      <List>
        {alerts.map((alert) => (
          <ListItem key={alert.id}>
            <ListItemIcon>
              {getAlertIcon(alert.type)}
            </ListItemIcon>
            <ListItemText
              primary={alert.message}
              secondary={new Date(alert.timestamp).toLocaleString()}
            />
            <Box>
              <Chip
                label={alert.type}
                color={getAlertColor(alert.type)}
                size="small"
                sx={{ mr: 1 }}
              />
              <IconButton
                size="small"
                onClick={() => onAlertAction(alert.id, 'acknowledge')}
              >
                <CheckCircle />
              </IconButton>
            </Box>
          </ListItem>
        ))}

        {alerts.length === 0 && (
          <ListItem>
            <ListItemText
              primary="No active alerts"
              secondary="System is running normally"
            />
          </ListItem>
        )}
      </List>
    </Paper>
  );
};
