import React from 'react';
import {
  Box,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  Chip
} from '@mui/material';
import {
  Warning,
  Error,
  Info,
  CheckCircle,
  Check,
  Clear
} from '@mui/icons-material';

interface Alert {
  id: string;
  type: 'warning' | 'error' | 'info';
  message: string;
  timestamp: string;
  status: 'active' | 'acknowledged' | 'resolved';
  priority: 'high' | 'medium' | 'low';
  source: string;
  details?: Record<string, unknown>;
}

interface SmartAlertSystemProps {
  alerts: Alert[];
  onAlertAction: (alertId: string, action: 'acknowledge' | 'resolve' | 'dismiss') => void;
}

export const SmartAlertSystem: React.FC<SmartAlertSystemProps> = ({ alerts, onAlertAction }) => {
  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'error':
        return <Error color="error" />;
      case 'warning':
        return <Warning color="warning" />;
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
