import React, { useState } from 'react';
import {
  Box,
  Stepper,
  Step,
  StepLabel,
  Button,
  Typography,
  Card,
  CardContent,
  Grid,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Autocomplete,
  Alert,
} from '@mui/material';
import { useQuery, useMutation } from 'react-query';
import axios from 'axios';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider, DatePicker, TimePicker } from '@mui/x-date-pickers';
import { ar } from 'date-fns/locale';

const steps = ['اختيار التخصص والطبيب', 'اختيار الموعد', 'تأكيد الحجز'];

interface Doctor {
  id: number;
  name: string;
  specialty: string;
  rating: number;
  availableDays: string[];
}

interface Specialty {
  id: number;
  name: string;
}

export default function BookAppointment() {
  const [activeStep, setActiveStep] = useState(0);
  const [specialty, setSpecialty] = useState<Specialty | null>(null);
  const [doctor, setDoctor] = useState<Doctor | null>(null);
  const [date, setDate] = useState<Date | null>(null);
  const [time, setTime] = useState<Date | null>(null);
  const [reason, setReason] = useState('');

  // استعلام التخصصات
  const { data: specialties } = useQuery('specialties', () =>
    axios.get('/api/specialties/').then((res) => res.data)
  );

  // استعلام الأطباء حسب التخصص
  const { data: doctors } = useQuery(
    ['doctors', specialty?.id],
    () => axios.get(`/api/doctors/?specialty=${specialty?.id}`).then((res) => res.data),
    { enabled: !!specialty }
  );

  // استعلام المواعيد المتاحة
  const { data: availableSlots } = useQuery(
    ['slots', doctor?.id, date],
    () =>
      axios
        .get(`/api/appointments/available-slots/`, {
          params: {
            doctor_id: doctor?.id,
            date: date?.toISOString().split('T')[0],
          },
        })
        .then((res) => res.data),
    { enabled: !!doctor && !!date }
  );

  // حجز الموعد
  const bookAppointment = useMutation(
    (appointmentData: any) =>
      axios.post('/api/appointments/', appointmentData),
    {
      onSuccess: () => {
        setActiveStep(3); // الانتقال إلى رسالة النجاح
      },
    }
  );

  const handleNext = () => {
    if (activeStep === 2) {
      bookAppointment.mutate({
        doctor_id: doctor?.id,
        date: date?.toISOString().split('T')[0],
        time: time?.toISOString().split('T')[1].split('.')[0],
        reason,
      });
    } else {
      setActiveStep((prevStep) => prevStep + 1);
    }
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const getStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Box sx={{ p: 2 }}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <Autocomplete
                    options={specialties || []}
                    getOptionLabel={(option) => option.name}
                    value={specialty}
                    onChange={(_, newValue) => {
                      setSpecialty(newValue);
                      setDoctor(null);
                    }}
                    renderInput={(params) => (
                      <TextField {...params} label="اختر التخصص" />
                    )}
                  />
                </FormControl>
              </Grid>
              {specialty && (
                <Grid item xs={12}>
                  <FormControl fullWidth>
                    <Autocomplete
                      options={doctors || []}
                      getOptionLabel={(option) => `${option.name} (${option.rating} ⭐)`}
                      value={doctor}
                      onChange={(_, newValue) => setDoctor(newValue)}
                      renderInput={(params) => (
                        <TextField {...params} label="اختر الطبيب" />
                      )}
                    />
                  </FormControl>
                </Grid>
              )}
            </Grid>
          </Box>
        );

      case 1:
        return (
          <Box sx={{ p: 2 }}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ar}>
                  <DatePicker
                    label="اختر التاريخ"
                    value={date}
                    onChange={(newValue) => setDate(newValue)}
                    disablePast
                    slots={{
                      textField: (params) => <TextField {...params} fullWidth />,
                    }}
                  />
                </LocalizationProvider>
              </Grid>
              {date && (
                <Grid item xs={12} md={6}>
                  <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ar}>
                    <TimePicker
                      label="اختر الوقت"
                      value={time}
                      onChange={(newValue) => setTime(newValue)}
                      slots={{
                        textField: (params) => <TextField {...params} fullWidth />,
                      }}
                    />
                  </LocalizationProvider>
                </Grid>
              )}
            </Grid>
          </Box>
        );

      case 2:
        return (
          <Box sx={{ p: 2 }}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      تفاصيل الموعد
                    </Typography>
                    <Typography>الطبيب: {doctor?.name}</Typography>
                    <Typography>
                      التاريخ: {date?.toLocaleDateString('ar-SA')}
                    </Typography>
                    <Typography>
                      الوقت: {time?.toLocaleTimeString('ar-SA')}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  label="سبب الزيارة"
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                />
              </Grid>
            </Grid>
          </Box>
        );

      case 3:
        return (
          <Box sx={{ p: 2 }}>
            <Alert severity="success">
              تم حجز موعدك بنجاح! سيتم إرسال تفاصيل الموعد إلى بريدك الإلكتروني.
            </Alert>
          </Box>
        );

      default:
        return 'Unknown step';
    }
  };

  return (
    <Box sx={{ width: '100%', p: 3 }}>
      <Typography variant="h4" gutterBottom align="center">
        حجز موعد جديد
      </Typography>
      <Stepper activeStep={activeStep} sx={{ pt: 3, pb: 5 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      {getStepContent(activeStep)}
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 3 }}>
        {activeStep !== 0 && activeStep !== 3 && (
          <Button onClick={handleBack} sx={{ mr: 1 }}>
            رجوع
          </Button>
        )}
        {activeStep !== 3 && (
          <Button
            variant="contained"
            onClick={handleNext}
            disabled={
              (activeStep === 0 && !doctor) ||
              (activeStep === 1 && (!date || !time)) ||
              (activeStep === 2 && !reason)
            }
          >
            {activeStep === steps.length - 1 ? 'تأكيد الحجز' : 'التالي'}
          </Button>
        )}
      </Box>
    </Box>
  );
}
