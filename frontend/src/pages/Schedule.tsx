import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  Add,
  Edit,
  Delete,
  Event,
  AccessTime,
  Person,
} from '@mui/icons-material';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { arSA } from 'date-fns/locale';
import { useSchedule } from '../hooks/useSchedule';

interface Appointment {
  id: string;
  patientName: string;
  date: Date;
  time: string;
  type: string;
  status: 'scheduled' | 'completed' | 'cancelled';
}

const Schedule: React.FC = () => {
  const { appointments, addAppointment, updateAppointment, deleteAppointment } = useSchedule();
  const [selectedDate, setSelectedDate] = useState<Date | null>(new Date());
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedAppointment, setSelectedAppointment] = useState<Appointment | null>(null);
  const [formData, setFormData] = useState({
    patientName: '',
    date: new Date(),
    time: '',
    type: '',
    status: 'scheduled' as const,
  });

  const handleOpenDialog = (appointment?: Appointment) => {
    if (appointment) {
      setSelectedAppointment(appointment);
      setFormData({
        patientName: appointment.patientName,
        date: new Date(appointment.date),
        time: appointment.time,
        type: appointment.type,
        status: appointment.status,
      });
    } else {
      setSelectedAppointment(null);
      setFormData({
        patientName: '',
        date: new Date(),
        time: '',
        type: '',
        status: 'scheduled',
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedAppointment(null);
  };

  const handleSubmit = () => {
    if (selectedAppointment) {
      updateAppointment(selectedAppointment.id, formData);
    } else {
      addAppointment(formData);
    }
    handleCloseDialog();
  };

  const handleDelete = (id: string) => {
    deleteAppointment(id);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success.main';
      case 'cancelled':
        return 'error.main';
      default:
        return 'info.main';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">الجدول الزمني</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
        >
          موعد جديد
        </Button>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2 }}>
            <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={arSA}>
              <DatePicker
                label="اختر التاريخ"
                value={selectedDate}
                onChange={(newValue) => setSelectedDate(newValue)}
                sx={{ width: '100%' }}
              />
            </LocalizationProvider>

            <Box sx={{ mt: 3 }}>
              <Typography variant="h6" gutterBottom>
                إحصائيات اليوم
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Card>
                    <CardContent>
                      <Typography color="textSecondary">المواعيد</Typography>
                      <Typography variant="h4">8</Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={6}>
                  <Card>
                    <CardContent>
                      <Typography color="textSecondary">مكتملة</Typography>
                      <Typography variant="h4">5</Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={9}>
          <Paper sx={{ p: 2 }}>
            {appointments.map((appointment) => (
              <Card key={appointment.id} sx={{ mb: 2 }}>
                <CardContent>
                  <Grid container alignItems="center" spacing={2}>
                    <Grid item xs={12} sm={4}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Person sx={{ mr: 1 }} />
                        <Typography>{appointment.patientName}</Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={6} sm={3}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Event sx={{ mr: 1 }} />
                        <Typography>
                          {new Date(appointment.date).toLocaleDateString('ar-SA')}
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={6} sm={2}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <AccessTime sx={{ mr: 1 }} />
                        <Typography>{appointment.time}</Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={6} sm={2}>
                      <Typography
                        sx={{
                          color: getStatusColor(appointment.status),
                          textAlign: 'center',
                        }}
                      >
                        {appointment.status}
                      </Typography>
                    </Grid>
                    <Grid item xs={6} sm={1}>
                      <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                        <IconButton
                          size="small"
                          onClick={() => handleOpenDialog(appointment)}
                        >
                          <Edit />
                        </IconButton>
                        <IconButton
                          size="small"
                          onClick={() => handleDelete(appointment.id)}
                        >
                          <Delete />
                        </IconButton>
                      </Box>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            ))}
          </Paper>
        </Grid>
      </Grid>

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {selectedAppointment ? 'تعديل موعد' : 'موعد جديد'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="اسم المريض"
                  value={formData.patientName}
                  onChange={(e) =>
                    setFormData({ ...formData, patientName: e.target.value })
                  }
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={arSA}>
                  <DatePicker
                    label="التاريخ"
                    value={formData.date}
                    onChange={(newValue) =>
                      setFormData({ ...formData, date: newValue || new Date() })
                    }
                    sx={{ width: '100%' }}
                  />
                </LocalizationProvider>
              </Grid>
              <Grid item xs={12} sm={6}>
                <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={arSA}>
                  <TimePicker
                    label="الوقت"
                    value={formData.time}
                    onChange={(newValue) =>
                      setFormData({
                        ...formData,
                        time: newValue?.toLocaleTimeString() || '',
                      })
                    }
                    sx={{ width: '100%' }}
                  />
                </LocalizationProvider>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="نوع الموعد"
                  value={formData.type}
                  onChange={(e) =>
                    setFormData({ ...formData, type: e.target.value })
                  }
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>الحالة</InputLabel>
                  <Select
                    value={formData.status}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        status: e.target.value as 'scheduled' | 'completed' | 'cancelled',
                      })
                    }
                  >
                    <MenuItem value="scheduled">مجدول</MenuItem>
                    <MenuItem value="completed">مكتمل</MenuItem>
                    <MenuItem value="cancelled">ملغي</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>إلغاء</Button>
          <Button onClick={handleSubmit} variant="contained">
            {selectedAppointment ? 'تحديث' : 'إضافة'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Schedule;
