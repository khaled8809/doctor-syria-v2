import React, { useState } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Button,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  CircularProgress,
} from '@mui/material';
import {
  Person,
  Event,
  LocalHospital,
  Message,
  VideoCall,
  Edit,
  Add,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { useSnackbar } from 'notistack';
import { format } from 'date-fns';

interface Patient {
  id: number;
  name: string;
  age: number;
  gender: string;
  condition: string;
  lastVisit: string;
  nextAppointment?: string;
  medicalHistory: string[];
  prescriptions: {
    id: number;
    medication: string;
    dosage: string;
    frequency: string;
    startDate: string;
    endDate: string;
  }[];
}

interface Appointment {
  id: number;
  patientName: string;
  patientId: number;
  dateTime: string;
  type: 'regular' | 'follow_up' | 'emergency';
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
  notes?: string;
}

const DoctorDashboard = () => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null);
  const [newAppointmentDialog, setNewAppointmentDialog] = useState(false);
  const { enqueueSnackbar } = useSnackbar();
  const queryClient = useQueryClient();

  // Fetch doctor's patients
  const { data: patients, isLoading: loadingPatients } = useQuery<Patient[]>(
    'doctor-patients',
    () => axios.get('/api/doctor/patients/').then((res) => res.data)
  );

  // Fetch appointments
  const { data: appointments, isLoading: loadingAppointments } = useQuery<
    Appointment[]
  >('doctor-appointments', () =>
    axios.get('/api/doctor/appointments/').then((res) => res.data)
  );

  // Add new appointment
  const addAppointmentMutation = useMutation(
    (newAppointment: Partial<Appointment>) =>
      axios.post('/api/doctor/appointments/', newAppointment),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('doctor-appointments');
        enqueueSnackbar('Appointment scheduled successfully', {
          variant: 'success',
        });
        setNewAppointmentDialog(false);
      },
    }
  );

  // Add prescription
  const addPrescriptionMutation = useMutation(
    (data: { patientId: number; prescription: any }) =>
      axios.post(`/api/doctor/patients/${data.patientId}/prescriptions/`, data.prescription),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('doctor-patients');
        enqueueSnackbar('Prescription added successfully', {
          variant: 'success',
        });
      },
    }
  );

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setSelectedTab(newValue);
  };

  const renderPatientsList = () => (
    <Paper sx={{ p: 2 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">My Patients</Typography>
        <Button startIcon={<Add />} variant="contained">
          Add Patient
        </Button>
      </Box>
      <List>
        {patients?.map((patient) => (
          <ListItem
            key={patient.id}
            button
            onClick={() => setSelectedPatient(patient)}
          >
            <ListItemAvatar>
              <Avatar>
                <Person />
              </Avatar>
            </ListItemAvatar>
            <ListItemText
              primary={patient.name}
              secondary={`Last visit: ${format(
                new Date(patient.lastVisit),
                'MMM d, yyyy'
              )}`}
            />
            {patient.nextAppointment && (
              <Chip
                label={`Next: ${format(
                  new Date(patient.nextAppointment),
                  'MMM d'
                )}`}
                color="primary"
                size="small"
              />
            )}
          </ListItem>
        ))}
      </List>
    </Paper>
  );

  const renderAppointments = () => (
    <Paper sx={{ p: 2 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Today's Appointments</Typography>
        <Button
          startIcon={<Add />}
          variant="contained"
          onClick={() => setNewAppointmentDialog(true)}
        >
          New Appointment
        </Button>
      </Box>
      <List>
        {appointments?.map((appointment) => (
          <ListItem key={appointment.id}>
            <ListItemText
              primary={appointment.patientName}
              secondary={format(
                new Date(appointment.dateTime),
                'HH:mm - MMM d, yyyy'
              )}
            />
            <Box>
              <Chip
                label={appointment.type}
                color={
                  appointment.type === 'emergency' ? 'error' : 'primary'
                }
                size="small"
                sx={{ mr: 1 }}
              />
              <Chip
                label={appointment.status}
                color={
                  appointment.status === 'completed'
                    ? 'success'
                    : appointment.status === 'cancelled'
                    ? 'error'
                    : 'default'
                }
                size="small"
              />
              <IconButton>
                <Edit />
              </IconButton>
              <IconButton>
                <VideoCall />
              </IconButton>
            </Box>
          </ListItem>
        ))}
      </List>
    </Paper>
  );

  const renderPatientDetails = () => (
    selectedPatient && (
      <Paper sx={{ p: 2 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">{selectedPatient.name}</Typography>
          <Button startIcon={<Message />} variant="outlined">
            Send Message
          </Button>
        </Box>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Personal Information
                </Typography>
                <Typography>Age: {selectedPatient.age}</Typography>
                <Typography>Gender: {selectedPatient.gender}</Typography>
                <Typography>
                  Condition: {selectedPatient.condition}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Medical History
                </Typography>
                <List dense>
                  {selectedPatient.medicalHistory.map((item, index) => (
                    <ListItem key={index}>
                      <ListItemText primary={item} />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Box
                  display="flex"
                  justifyContent="space-between"
                  alignItems="center"
                >
                  <Typography color="textSecondary" gutterBottom>
                    Current Prescriptions
                  </Typography>
                  <Button
                    startIcon={<Add />}
                    size="small"
                    onClick={() => {
                      // Add prescription logic
                    }}
                  >
                    Add Prescription
                  </Button>
                </Box>
                <List dense>
                  {selectedPatient.prescriptions.map((prescription) => (
                    <ListItem key={prescription.id}>
                      <ListItemText
                        primary={prescription.medication}
                        secondary={`${prescription.dosage} - ${prescription.frequency}`}
                      />
                      <Typography variant="body2" color="textSecondary">
                        {format(new Date(prescription.startDate), 'MMM d')} -{' '}
                        {format(new Date(prescription.endDate), 'MMM d')}
                      </Typography>
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Paper>
    )
  );

  if (loadingPatients || loadingAppointments) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="400px"
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Grid container spacing={3}>
        {/* Header */}
        <Grid item xs={12}>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h4">Doctor Dashboard</Typography>
            <Button
              variant="contained"
              startIcon={<VideoCall />}
              color="primary"
            >
              Start Consultation
            </Button>
          </Box>
        </Grid>

        {/* Stats Cards */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Patients
              </Typography>
              <Typography variant="h4">{patients?.length || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Today's Appointments
              </Typography>
              <Typography variant="h4">
                {appointments?.filter((apt) =>
                  format(new Date(apt.dateTime), 'yyyy-MM-dd') ===
                  format(new Date(), 'yyyy-MM-dd')
                ).length || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Pending Reports
              </Typography>
              <Typography variant="h4">5</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Messages
              </Typography>
              <Typography variant="h4">3</Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Main Content */}
        <Grid item xs={12}>
          <Paper sx={{ width: '100%', mb: 2 }}>
            <Tabs
              value={selectedTab}
              onChange={handleTabChange}
              variant="fullWidth"
            >
              <Tab icon={<Person />} label="Patients" />
              <Tab icon={<Event />} label="Appointments" />
              <Tab icon={<LocalHospital />} label="Patient Details" />
            </Tabs>
          </Paper>

          <Box sx={{ mt: 2 }}>
            {selectedTab === 0 && renderPatientsList()}
            {selectedTab === 1 && renderAppointments()}
            {selectedTab === 2 && renderPatientDetails()}
          </Box>
        </Grid>
      </Grid>

      {/* New Appointment Dialog */}
      <Dialog
        open={newAppointmentDialog}
        onClose={() => setNewAppointmentDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Schedule New Appointment</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Patient"
                select
                SelectProps={{
                  native: true,
                }}
                variant="outlined"
              >
                {patients?.map((patient) => (
                  <option key={patient.id} value={patient.id}>
                    {patient.name}
                  </option>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Date & Time"
                type="datetime-local"
                variant="outlined"
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Type"
                select
                SelectProps={{
                  native: true,
                }}
                variant="outlined"
              >
                <option value="regular">Regular</option>
                <option value="follow_up">Follow-up</option>
                <option value="emergency">Emergency</option>
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Notes"
                multiline
                rows={4}
                variant="outlined"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setNewAppointmentDialog(false)}>
            Cancel
          </Button>
          <Button
            variant="contained"
            color="primary"
            disabled={addAppointmentMutation.isLoading}
          >
            Schedule
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default DoctorDashboard;
