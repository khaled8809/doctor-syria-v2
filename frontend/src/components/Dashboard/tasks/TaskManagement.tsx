import React from 'react';
import {
  Box,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  Chip,
  IconButton,
  Avatar,
  ListItemAvatar,
  ListItemSecondaryAction
} from '@mui/material';
import {
  Assignment as AssignmentIcon,
  CheckCircle,
  Delete
} from '@mui/icons-material';
import { Task, User } from '../../../types/common';

interface TaskManagementProps {
  tasks: Task[];
  onTaskUpdate: (taskId: string, updates: any) => void;
}

export const TaskManagement: React.FC<TaskManagementProps> = ({ tasks, onTaskUpdate }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'in_progress':
        return 'warning';
      case 'pending':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Paper sx={{ p: 2, height: '100%' }}>
      <Typography variant="h6" gutterBottom>
        Task Management
      </Typography>

      <List>
        {tasks.map((task) => (
          <ListItem key={task.id}>
            <ListItemAvatar>
              <Avatar>
                <AssignmentIcon />
              </Avatar>
            </ListItemAvatar>
            <ListItemText
              primary={task.title}
              secondary={task.description}
            />
            <ListItemSecondaryAction>
              <Box display="flex" alignItems="center" gap={1}>
                <Chip
                  label={task.status}
                  color={getStatusColor(task.status)}
                  size="small"
                />
                <IconButton
                  edge="end"
                  onClick={() => onTaskUpdate(task.id, { status: 'completed' })}
                  disabled={task.status === 'completed'}
                >
                  <CheckCircle />
                </IconButton>
                <IconButton
                  edge="end"
                  onClick={() => onTaskUpdate(task.id, { deleted: true })}
                >
                  <Delete />
                </IconButton>
              </Box>
            </ListItemSecondaryAction>
          </ListItem>
        ))}

        {tasks.length === 0 && (
          <ListItem>
            <ListItemText
              primary="No tasks"
              secondary="All caught up!"
            />
          </ListItem>
        )}
      </List>
    </Paper>
  );
};
