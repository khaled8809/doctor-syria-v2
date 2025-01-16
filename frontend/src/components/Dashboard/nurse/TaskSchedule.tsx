import React, { useState } from 'react';
import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
  TimelineOppositeContent,
} from '@mui/lab';
import {
  Typography,
  Box,
  Checkbox,
  IconButton,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField
} from '@mui/material';
import {
  Assignment,
  AccessTime,
  Edit,
  Person,
  Room
} from '@mui/icons-material';

interface Task {
  id: string;
  title: string;
  description: string;
  patientName: string;
  roomNumber: string;
  time: string;
  priority: 'high' | 'medium' | 'low';
  status: 'pending' | 'completed' | 'overdue';
  notes?: string;
  assignedTo?: string;
  createdAt: string;
  updatedAt: string;
  completedAt?: string;
  category?: 'medication' | 'checkup' | 'procedure' | 'other';
  estimatedDuration?: number;
}

interface TaskScheduleProps {
  tasks: Task[];
  onTaskUpdate?: (taskId: string, updates: Partial<Task>) => void;
  onTaskComplete?: (taskId: string) => void;
  onTaskEdit?: (task: Task) => void;
  showCompleted?: boolean;
  filterByPriority?: ('high' | 'medium' | 'low')[];
  filterByStatus?: ('pending' | 'completed' | 'overdue')[];
}

export const TaskSchedule: React.FC<TaskScheduleProps> = ({
  tasks,
  onTaskUpdate,
  onTaskComplete,
  onTaskEdit,
  showCompleted,
  filterByPriority,
  filterByStatus,
}) => {
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [notes, setNotes] = useState('');

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      default:
        return 'info';
    }
  };

  const handleTaskComplete = (taskId: string) => {
    if (onTaskComplete) {
      onTaskComplete(taskId);
    }
    console.log('Task completed:', taskId);
  };

  const handleTaskEdit = (task: Task) => {
    setSelectedTask(task);
    setNotes(task.notes || '');
    setDialogOpen(true);
  };

  const handleDialogClose = () => {
    setDialogOpen(false);
    setSelectedTask(null);
    setNotes('');
  };

  const handleNotesSave = () => {
    if (selectedTask && onTaskUpdate) {
      onTaskUpdate(selectedTask.id, { notes });
    }
    handleDialogClose();
  };

  return (
    <>
      <Timeline position="right">
        {tasks
          .filter((task) => {
            if (filterByPriority && !filterByPriority.includes(task.priority)) {
              return false;
            }
            if (filterByStatus && !filterByStatus.includes(task.status)) {
              return false;
            }
            return true;
          })
          .map((task) => (
            <TimelineItem key={task.id}>
              <TimelineOppositeContent sx={{ flex: 0.2 }}>
                <Typography variant="caption" color="text.secondary">
                  {task.time}
                </Typography>
              </TimelineOppositeContent>
              <TimelineSeparator>
                <TimelineDot color={getPriorityColor(task.priority)}>
                  <Assignment />
                </TimelineDot>
                <TimelineConnector />
              </TimelineSeparator>
              <TimelineContent>
                <Box
                  sx={{
                    p: 2,
                    bgcolor: 'background.paper',
                    borderRadius: 1,
                    boxShadow: 1,
                    '&:hover': {
                      boxShadow: 2,
                    },
                  }}
                >
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="subtitle1">
                      {task.title}
                    </Typography>
                    <Box>
                      <Checkbox
                        checked={task.status === 'completed'}
                        onChange={() => handleTaskComplete(task.id)}
                      />
                      <IconButton size="small" onClick={() => handleTaskEdit(task)}>
                        <Edit />
                      </IconButton>
                    </Box>
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {task.description}
                  </Typography>
                  <Box sx={{ mt: 1, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    <Chip
                      icon={<Person />}
                      label={task.patientName}
                      size="small"
                      variant="outlined"
                    />
                    <Chip
                      icon={<Room />}
                      label={`غرفة ${task.roomNumber}`}
                      size="small"
                      variant="outlined"
                    />
                    <Chip
                      icon={<AccessTime />}
                      label={task.status}
                      size="small"
                      color={task.status === 'overdue' ? 'error' : 'default'}
                    />
                  </Box>
                </Box>
              </TimelineContent>
            </TimelineItem>
          ))}
      </Timeline>

      <Dialog open={dialogOpen} onClose={handleDialogClose} maxWidth="sm" fullWidth>
        <DialogTitle>
          تحديث المهمة: {selectedTask?.title}
        </DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            multiline
            rows={4}
            label="ملاحظات"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose}>إلغاء</Button>
          <Button onClick={handleNotesSave} variant="contained" color="primary">
            حفظ
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default TaskSchedule;
