import React from 'react';
import {
  Box,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  Chip,
  ListItemAvatar,
  Avatar,
  LinearProgress
} from '@mui/material';
import {
  Inventory as InventoryIcon,
  Warning,
  CheckCircle
} from '@mui/icons-material';
import { Resource } from '../../../types/common';

interface ResourceManagementProps {
  resources: Resource[];
}

export const ResourceManagement: React.FC<ResourceManagementProps> = ({ resources }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'available':
        return 'success';
      case 'low':
        return 'warning';
      case 'critical':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'available':
        return <CheckCircle color="success" />;
      case 'low':
      case 'critical':
        return <Warning color="error" />;
      default:
        return <InventoryIcon />;
    }
  };

  const getQuantityPercentage = (quantity: number) => {
    return Math.min(100, (quantity / 100) * 100);
  };

  return (
    <Paper sx={{ p: 2, height: '100%' }}>
      <Typography variant="h6" gutterBottom>
        Resource Management
      </Typography>

      <List>
        {resources.map((resource) => (
          <ListItem key={resource.id}>
            <ListItemAvatar>
              <Avatar>
                {getStatusIcon(resource.status)}
              </Avatar>
            </ListItemAvatar>
            <ListItemText
              primary={resource.name}
              secondary={
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    {resource.quantity} {resource.unit}
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={getQuantityPercentage(resource.quantity)}
                    color={getStatusColor(resource.status)}
                    sx={{ mt: 1, mb: 1 }}
                  />
                </Box>
              }
            />
            <Box>
              <Chip
                label={resource.status}
                color={getStatusColor(resource.status)}
                size="small"
              />
            </Box>
          </ListItem>
        ))}

        {resources.length === 0 && (
          <ListItem>
            <ListItemText
              primary="No resources"
              secondary="Add resources to monitor inventory"
            />
          </ListItem>
        )}
      </List>
    </Paper>
  );
};
