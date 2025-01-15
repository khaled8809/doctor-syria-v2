import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Switch,
  FormControlLabel,
  Grid,
  Badge,
  Alert,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Notifications as NotificationsIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import { TimePicker } from '@mui/x-date-pickers';
import { useTranslation } from 'react-i18next';
import { format } from 'date-fns';
import { ar } from 'date-fns/locale';

interface Reminder {
  id: string;
  medicationName: string;
  dosage: string;
  time: Date;
  active: boolean;
  taken: boolean;
}

const MedicationReminder: React.FC = () => {
  const { t } = useTranslation();
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [currentReminder, setCurrentReminder] = useState<Reminder | null>(null);
  const [notificationPermission, setNotificationPermission] = useState<boolean>(false);

  useEffect(() => {
    // Check for notification permission
    if ('Notification' in window) {
      if (Notification.permission === 'granted') {
        setNotificationPermission(true);
      }
    }

    // Load reminders from local storage
    const savedReminders = localStorage.getItem('medicationReminders');
    if (savedReminders) {
      setReminders(JSON.parse(savedReminders));
    }

    // Start checking for reminders
    const interval = setInterval(checkReminders, 60000);
    return () => clearInterval(interval);
  }, []);

  const requestNotificationPermission = async () => {
    if ('Notification' in window) {
      const permission = await Notification.requestPermission();
      setNotificationPermission(permission === 'granted');
    }
  };

  const checkReminders = () => {
    const now = new Date();
    reminders.forEach(reminder => {
      if (reminder.active && !reminder.taken) {
        const reminderTime = new Date(reminder.time);
        if (
          reminderTime.getHours() === now.getHours() &&
          reminderTime.getMinutes() === now.getMinutes()
        ) {
          sendNotification(reminder);
        }
      }
    });
  };

  const sendNotification = (reminder: Reminder) => {
    if (notificationPermission) {
      new Notification(t('medications.reminder.title'), {
        body: t('medications.reminder.body', {
          name: reminder.medicationName,
          dosage: reminder.dosage
        }),
        icon: '/assets/images/logo.png'
      });
    }
  };

  const handleSaveReminder = (reminder: Reminder) => {
    if (currentReminder) {
      // Edit existing reminder
      setReminders(prev =>
        prev.map(r => (r.id === currentReminder.id ? reminder : r))
      );
    } else {
      // Add new reminder
      setReminders(prev => [...prev, { ...reminder, id: Date.now().toString() }]);
    }
    setOpenDialog(false);
    setCurrentReminder(null);
  };

  const handleDeleteReminder = (id: string) => {
    setReminders(prev => prev.filter(r => r.id !== id));
  };

  const handleToggleReminder = (id: string) => {
    setReminders(prev =>
      prev.map(r =>
        r.id === id ? { ...r, active: !r.active } : r
      )
    );
  };

  const handleTakeReminder = (id: string) => {
    setReminders(prev =>
      prev.map(r =>
        r.id === id ? { ...r, taken: true } : r
      )
    );
  };

  const ReminderDialog: React.FC = () => {
    const [formData, setFormData] = useState(
      currentReminder || {
        medicationName: '',
        dosage: '',
        time: new Date(),
        active: true,
        taken: false,
      }
    );

    return (
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          {currentReminder
            ? t('medications.reminder.edit')
            : t('medications.reminder.add')}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label={t('medications.reminder.medicationName')}
                value={formData.medicationName}
                onChange={e =>
                  setFormData(prev => ({ ...prev, medicationName: e.target.value }))
                }
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label={t('medications.reminder.dosage')}
                value={formData.dosage}
                onChange={e =>
                  setFormData(prev => ({ ...prev, dosage: e.target.value }))
                }
              />
            </Grid>
            <Grid item xs={12}>
              <TimePicker
                label={t('medications.reminder.time')}
                value={formData.time}
                onChange={newValue =>
                  setFormData(prev => ({ ...prev, time: newValue || new Date() }))
                }
              />
            </Grid>
            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={formData.active}
                    onChange={e =>
                      setFormData(prev => ({ ...prev, active: e.target.checked }))
                    }
                  />
                }
                label={t('medications.reminder.active')}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>
            {t('common.cancel')}
          </Button>
          <Button
            onClick={() => handleSaveReminder(formData)}
            variant="contained"
            color="primary"
          >
            {t('common.save')}
          </Button>
        </DialogActions>
      </Dialog>
    );
  };

  return (
    <Box>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h5">{t('medications.reminder.title')}</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            setCurrentReminder(null);
            setOpenDialog(true);
          }}
        >
          {t('medications.reminder.addNew')}
        </Button>
      </Box>

      {!notificationPermission && (
        <Alert
          severity="warning"
          action={
            <Button color="inherit" size="small" onClick={requestNotificationPermission}>
              {t('medications.reminder.enableNotifications')}
            </Button>
          }
          sx={{ mb: 3 }}
        >
          {t('medications.reminder.notificationsDisabled')}
        </Alert>
      )}

      <Grid container spacing={3}>
        {reminders.map(reminder => (
          <Grid item xs={12} sm={6} md={4} key={reminder.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="h6">{reminder.medicationName}</Typography>
                  <Box>
                    <IconButton
                      size="small"
                      onClick={() => {
                        setCurrentReminder(reminder);
                        setOpenDialog(true);
                      }}
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleDeleteReminder(reminder.id)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                </Box>
                <Typography color="textSecondary" gutterBottom>
                  {reminder.dosage}
                </Typography>
                <Typography variant="body2">
                  {format(new Date(reminder.time), 'HH:mm', { locale: ar })}
                </Typography>
                <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={reminder.active}
                        onChange={() => handleToggleReminder(reminder.id)}
                        size="small"
                      />
                    }
                    label={t('medications.reminder.active')}
                  />
                  {!reminder.taken && (
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<CheckCircleIcon />}
                      onClick={() => handleTakeReminder(reminder.id)}
                    >
                      {t('medications.reminder.take')}
                    </Button>
                  )}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <ReminderDialog />
    </Box>
  );
};

export default MedicationReminder;
