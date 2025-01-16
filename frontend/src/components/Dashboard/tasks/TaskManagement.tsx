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
  ListItemSecondaryAction,
  Menu,
  MenuItem,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  Assignment as AssignmentIcon,
  CheckCircle,
  Delete,
  Edit,
  MoreVert,
} from '@mui/icons-material';
import { Task } from '../../../types/task';
import { User } from '../../../types/user';

interface TaskManagementProps {
  tasks: Task[];
  onTaskUpdate: (taskId: string, updates: Partial<Task>) => void;
  onTaskDelete?: (taskId: string) => void;
  onTaskCreate?: (task: Omit<Task, 'id'>) => void;
  users?: User[];
  showCompleted?: boolean;
  filterByPriority?: ('high' | 'medium' | 'low')[];
  filterByStatus?: ('pending' | 'in_progress' | 'completed')[];
}

export const TaskManagement: React.FC<TaskManagementProps> = ({
  tasks,
  onTaskUpdate,
  onTaskDelete,
  onTaskCreate,
  users,
  showCompleted = true,
  filterByPriority,
  filterByStatus,
}) => {
  const [selectedTask, setSelectedTask] = React.useState<Task | null>(null);
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [editMode, setEditMode] = React.useState(false);

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>, task: Task) => {
    setSelectedTask(task);
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleEditClick = () => {
    setDialogOpen(true);
    setEditMode(true);
    handleMenuClose();
  };

  const handleDeleteClick = () => {
    if (selectedTask && onTaskDelete) {
      onTaskDelete(selectedTask.id);
    }
    handleMenuClose();
  };

  const handleDialogClose = () => {
    setDialogOpen(false);
    setSelectedTask(null);
    setEditMode(false);
  };

  const handleTaskSave = (updatedTask: Partial<Task>) => {
    if (editMode && selectedTask) {
      onTaskUpdate(selectedTask.id, updatedTask);
    } else if (onTaskCreate) {
      onTaskCreate(updatedTask as Omit<Task, 'id'>);
    }
    handleDialogClose();
  };

  const getStatusColor = (status: Task['status']) => {
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

  const filteredTasks = tasks.filter((task) => {
    if (!showCompleted && task.status === 'completed') return false;
    if (filterByPriority && !filterByPriority.includes(task.priority)) return false;
    if (filterByStatus && !filterByStatus.includes(task.status)) return false;
    return true;
  });

  return (
    <Paper sx={{ p: 2, height: '100%' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6">
          Task Management
        </Typography>
        {onTaskCreate && (
          <Button
            variant="contained"
            color="primary"
            onClick={() => {
              setEditMode(false);
              setDialogOpen(true);
            }}
          >
            Add Task
          </Button>
        )}
      </Box>

      <List>
        {filteredTasks.map((task) => (
          <ListItem
            key={task.id}
            sx={{
              mb: 1,
              bgcolor: 'background.paper',
              borderRadius: 1,
              '&:hover': {
                bgcolor: 'action.hover',
              },
            }}
          >
            <ListItemAvatar>
              <Avatar>
                <AssignmentIcon />
              </Avatar>
            </ListItemAvatar>
            <ListItemText
              primary={task.title}
              secondary={
                <Box sx={{ mt: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    {task.description}
                  </Typography>
                  <Box sx={{ mt: 1, display: 'flex', gap: 1 }}>
                    <Chip
                      label={task.status}
                      size="small"
                      color={getStatusColor(task.status)}
                    />
                    <Chip
                      label={task.priority}
                      size="small"
                      color={task.priority === 'high' ? 'error' : task.priority === 'medium' ? 'warning' : 'default'}
                    />
                    {task.assignedTo && (
                      <Chip
                        label={task.assignedTo}
                        size="small"
                        variant="outlined"
                      />
                    )}
                  </Box>
                </Box>
              }
            />
            <ListItemSecondaryAction>
              <IconButton edge="end" onClick={(e) => handleMenuClick(e, task)}>
                <MoreVert />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleEditClick}>
          <Edit sx={{ mr: 1 }} /> Edit
        </MenuItem>
        {onTaskDelete && (
          <MenuItem onClick={handleDeleteClick}>
            <Delete sx={{ mr: 1 }} /> Delete
          </MenuItem>
        )}
      </Menu>

      <Dialog
        open={dialogOpen}
        onClose={handleDialogClose}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          {editMode ? 'Edit Task' : 'Create Task'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Title"
              fullWidth
              defaultValue={selectedTask?.title}
              onChange={(e) => {
                if (selectedTask) {
                  setSelectedTask({ ...selectedTask, title: e.target.value });
                }
              }}
            />
            <TextField
              label="Description"
              fullWidth
              multiline
              rows={4}
              defaultValue={selectedTask?.description}
              onChange={(e) => {
                if (selectedTask) {
                  setSelectedTask({ ...selectedTask, description: e.target.value });
                }
              }}
            />
            <FormControl fullWidth>
              <InputLabel>Priority</InputLabel>
              <Select
                label="Priority"
                defaultValue={selectedTask?.priority || 'medium'}
                onChange={(e) => {
                  if (selectedTask) {
                    setSelectedTask({
                      ...selectedTask,
                      priority: e.target.value as Task['priority'],
                    });
                  }
                }}
              >
                <MenuItem value="high">High</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="low">Low</MenuItem>
              </Select>
            </FormControl>
            {users && (
              <FormControl fullWidth>
                <InputLabel>Assigned To</InputLabel>
                <Select
                  label="Assigned To"
                  defaultValue={selectedTask?.assignedTo || ''}
                  onChange={(e) => {
                    if (selectedTask) {
                      setSelectedTask({
                        ...selectedTask,
                        assignedTo: e.target.value as string,
                      });
                    }
                  }}
                >
                  {users.map((user) => (
                    <MenuItem key={user.id} value={user.id}>
                      {user.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose}>Cancel</Button>
          <Button
            onClick={() => handleTaskSave(selectedTask || {})}
            variant="contained"
            color="primary"
          >
            {editMode ? 'Save' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Paper>
  );
};

export default TaskManagement;
