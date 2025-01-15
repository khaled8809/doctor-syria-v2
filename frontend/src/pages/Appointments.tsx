import { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  IconButton,
  Tabs,
  Tab,
  Card,
  CardContent,
  Chip,
} from '@mui/material';
import {
  Add,
  Event,
  AccessTime,
  Person,
  Notes,
  Edit,
  Delete,
} from '@mui/icons-material';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { arDZ } from 'date-fns/locale';

interface Appointment {
  id: string;
  patientName: string;
  date: Date;
  time: string;
  type: string;
  status: 'scheduled' | 'completed' | 'cancelled';
  notes?: string;
}

const DUMMY_APPOINTMENTS: Appointment[] = [
  {
    id: '1',
    patientName: 'أحمد محمد',
    date: new Date('2025-01-15'),
    time: '10:00',
    type: 'كشف',
    status: 'scheduled',
    notes: 'كشف دوري',
  },
  {
    id: '2',
    patientName: 'سارة أحمد',
    date: new Date('2025-01-15'),
    time: '11:30',
    type: 'متابعة',
    status: 'scheduled',
  },
  // يمكن إضافة المزيد من البيانات الوهمية هنا
];

const Appointments = () => {
  const [appointments, setAppointments] = useState<Appointment[]>(DUMMY_APPOINTMENTS);
  const [openAddDialog, setOpenAddDialog] = useState(false);
  const [selectedDate, setSelectedDate] = useState<Date | null>(new Date());
  const [selectedTime, setSelectedTime] = useState<Date | null>(new Date());
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'scheduled':
        return 'primary';
      case 'completed':
        return 'success';
      case 'cancelled':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'scheduled':
        return 'مجدول';
      case 'completed':
        return 'مكتمل';
      case 'cancelled':
        return 'ملغي';
      default:
        return status;
    }
  };

  const AppointmentCard = ({ appointment }: { appointment: Appointment }) => (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6">{appointment.patientName}</Typography>
          <Chip
            label={getStatusLabel(appointment.status)}
            color={getStatusColor(appointment.status)}
            size="small"
          />
        </Box>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Event color="action" />
              <Typography variant="body2">
                {appointment.date.toLocaleDateString('ar-EG')}
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <AccessTime color="action" />
              <Typography variant="body2">{appointment.time}</Typography>
            </Box>
          </Grid>
        </Grid>
        {appointment.notes && (
          <Box sx={{ mt: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Notes color="action" />
              <Typography variant="body2">{appointment.notes}</Typography>
            </Box>
          </Box>
        )}
        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
          <IconButton size="small" color="primary">
            <Edit />
          </IconButton>
          <IconButton size="small" color="error">
            <Delete />
          </IconButton>
        </Box>
      </CardContent>
    </Card>
  );

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">المواعيد</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setOpenAddDialog(true)}
        >
          إضافة موعد
        </Button>
      </Box>

      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
        >
          <Tab label="اليوم" />
          <Tab label="الأسبوع" />
          <Tab label="الشهر" />
        </Tabs>
      </Paper>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          {appointments.map((appointment) => (
            <AppointmentCard key={appointment.id} appointment={appointment} />
          ))}
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, mb: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              ملخص المواعيد
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={4}>
                <Typography variant="h4" color="primary" align="center">
                  5
                </Typography>
                <Typography variant="body2" color="text.secondary" align="center">
                  اليوم
                </Typography>
              </Grid>
              <Grid item xs={4}>
                <Typography variant="h4" color="primary" align="center">
                  23
                </Typography>
                <Typography variant="body2" color="text.secondary" align="center">
                  الأسبوع
                </Typography>
              </Grid>
              <Grid item xs={4}>
                <Typography variant="h4" color="primary" align="center">
                  89
                </Typography>
                <Typography variant="body2" color="text.secondary" align="center">
                  الشهر
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>

      {/* Add Appointment Dialog */}
      <Dialog
        open={openAddDialog}
        onClose={() => setOpenAddDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>إضافة موعد جديد</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                select
                label="المريض"
                defaultValue=""
              >
                <MenuItem value="1">أحمد محمد</MenuItem>
                <MenuItem value="2">سارة أحمد</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={arDZ}>
                <DatePicker
                  label="التاريخ"
                  value={selectedDate}
                  onChange={(newValue) => setSelectedDate(newValue)}
                  slotProps={{ textField: { fullWidth: true } }}
                />
              </LocalizationProvider>
            </Grid>
            <Grid item xs={12} sm={6}>
              <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={arDZ}>
                <TimePicker
                  label="الوقت"
                  value={selectedTime}
                  onChange={(newValue) => setSelectedTime(newValue)}
                  slotProps={{ textField: { fullWidth: true } }}
                />
              </LocalizationProvider>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                select
                label="نوع الموعد"
                defaultValue=""
              >
                <MenuItem value="كشف">كشف</MenuItem>
                <MenuItem value="متابعة">متابعة</MenuItem>
                <MenuItem value="استشارة">استشارة</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="ملاحظات"
                multiline
                rows={3}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAddDialog(false)}>إلغاء</Button>
          <Button variant="contained" onClick={() => setOpenAddDialog(false)}>
            حفظ
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Appointments;
