import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack,
  Alert,
  IconButton,
  Chip,
} from '@mui/material';
import {
  Notifications,
  Add as AddIcon,
  Delete as DeleteIcon,
  Schedule as ScheduleIcon,
  NotificationsActive as NotificationsActiveIcon,
} from '@mui/icons-material';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { ar } from 'date-fns/locale';

interface Reminder {
  id: number;
  type: 'medication' | 'followUp' | 'test';
  title: string;
  description: string;
  datetime: Date;
  priority: 'low' | 'medium' | 'high';
  status: 'pending' | 'completed' | 'cancelled';
}

interface FollowUpReminderProps {
  patientId: number;
  diagnosis: {
    name: string;
    risk_level: number;
  };
  onReminderCreate: (reminder: Omit<Reminder, 'id'>) => Promise<void>;
  onReminderUpdate: (reminder: Reminder) => Promise<void>;
}

export default function FollowUpReminder({
  patientId,
  diagnosis,
  onReminderCreate,
  onReminderUpdate,
}: FollowUpReminderProps) {
  const [open, setOpen] = useState(false);
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [newReminder, setNewReminder] = useState<Partial<Reminder>>({
    type: 'followUp',
    priority: 'medium',
    status: 'pending',
    datetime: new Date(),
  });
  const [error, setError] = useState<string | null>(null);

  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    setOpen(false);
    setError(null);
    setNewReminder({
      type: 'followUp',
      priority: 'medium',
      status: 'pending',
      datetime: new Date(),
    });
  };

  const handleCreate = async () => {
    try {
      if (!newReminder.title || !newReminder.datetime) {
        setError('الرجاء إدخال جميع البيانات المطلوبة');
        return;
      }

      await onReminderCreate(newReminder as Omit<Reminder, 'id'>);
      handleClose();
    } catch (err) {
      setError('حدث خطأ أثناء إنشاء التذكير');
    }
  };

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

  const getReminderTypeIcon = (type: string) => {
    switch (type) {
      case 'medication':
        return <NotificationsActiveIcon />;
      case 'test':
        return <ScheduleIcon />;
      default:
        return <Notifications />;
    }
  };

  return (
    <>
      <Card variant="outlined" sx={{ mt: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">
              المتابعة والتذكيرات
            </Typography>
            <Button
              startIcon={<AddIcon />}
              variant="contained"
              onClick={handleOpen}
            >
              إضافة تذكير
            </Button>
          </Box>

          <Stack spacing={2}>
            {reminders.map((reminder) => (
              <Card key={reminder.id} variant="outlined">
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {getReminderTypeIcon(reminder.type)}
                      <Typography variant="subtitle1">
                        {reminder.title}
                      </Typography>
                    </Box>
                    <Box>
                      <Chip
                        label={reminder.priority}
                        color={getPriorityColor(reminder.priority)}
                        size="small"
                        sx={{ mr: 1 }}
                      />
                      <IconButton
                        size="small"
                        onClick={() => {
                          // Handle delete
                        }}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Box>
                  </Box>

                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {reminder.description}
                  </Typography>

                  <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                    {new Date(reminder.datetime).toLocaleString('ar-SA')}
                  </Typography>
                </CardContent>
              </Card>
            ))}
          </Stack>

          {reminders.length === 0 && (
            <Typography color="text.secondary" align="center">
              لا توجد تذكيرات حالياً
            </Typography>
          )}
        </CardContent>
      </Card>

      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>إضافة تذكير جديد</DialogTitle>
        <DialogContent>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Stack spacing={2} sx={{ mt: 2 }}>
            <FormControl fullWidth>
              <InputLabel>نوع التذكير</InputLabel>
              <Select
                value={newReminder.type}
                label="نوع التذكير"
                onChange={(e) => setNewReminder({ ...newReminder, type: e.target.value })}
              >
                <MenuItem value="medication">دواء</MenuItem>
                <MenuItem value="followUp">متابعة</MenuItem>
                <MenuItem value="test">فحص</MenuItem>
              </Select>
            </FormControl>

            <TextField
              label="العنوان"
              fullWidth
              value={newReminder.title || ''}
              onChange={(e) => setNewReminder({ ...newReminder, title: e.target.value })}
            />

            <TextField
              label="الوصف"
              fullWidth
              multiline
              rows={3}
              value={newReminder.description || ''}
              onChange={(e) => setNewReminder({ ...newReminder, description: e.target.value })}
            />

            <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ar}>
              <DateTimePicker
                label="الموعد"
                value={newReminder.datetime}
                onChange={(newValue) => {
                  if (newValue) {
                    setNewReminder({ ...newReminder, datetime: newValue });
                  }
                }}
              />
            </LocalizationProvider>

            <FormControl fullWidth>
              <InputLabel>الأولوية</InputLabel>
              <Select
                value={newReminder.priority}
                label="الأولوية"
                onChange={(e) => setNewReminder({ ...newReminder, priority: e.target.value })}
              >
                <MenuItem value="low">منخفضة</MenuItem>
                <MenuItem value="medium">متوسطة</MenuItem>
                <MenuItem value="high">عالية</MenuItem>
              </Select>
            </FormControl>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>إلغاء</Button>
          <Button onClick={handleCreate} variant="contained">
            إضافة
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
