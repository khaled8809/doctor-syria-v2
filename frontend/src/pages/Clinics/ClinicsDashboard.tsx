import React, { useState } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Button,
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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  LocalHospital,
  Person,
  Event,
  AttachMoney,
  Add,
  Edit,
  Delete,
  LocationOn,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { useSnackbar } from 'notistack';
import { format } from 'date-fns';

interface Clinic {
  id: number;
  name: string;
  location: string;
  specialization: string;
  doctors: {
    id: number;
    name: string;
    specialization: string;
    schedule: {
      day: string;
      startTime: string;
      endTime: string;
    }[];
  }[];
  services: {
    id: number;
    name: string;
    price: number;
    duration: number;
  }[];
  equipment: {
    id: number;
    name: string;
    status: 'operational' | 'maintenance' | 'out_of_order';
    lastMaintenance: string;
  }[];
}

interface Appointment {
  id: number;
  patientName: string;
  doctorName: string;
  service: string;
  dateTime: string;
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
  payment: {
    amount: number;
    status: 'pending' | 'paid' | 'refunded';
  };
}

const ClinicsDashboard = () => {
  const [selectedClinic, setSelectedClinic] = useState<Clinic | null>(null);
  const [newAppointmentDialog, setNewAppointmentDialog] = useState(false);
  const [newServiceDialog, setNewServiceDialog] = useState(false);
  const { enqueueSnackbar } = useSnackbar();
  const queryClient = useQueryClient();

  // Fetch clinics data
  const { data: clinics, isLoading: loadingClinics } = useQuery<Clinic[]>(
    'clinics',
    () => axios.get('/api/clinics/').then((res) => res.data)
  );

  // Fetch appointments
  const { data: appointments, isLoading: loadingAppointments } = useQuery<
    Appointment[]
  >('clinic-appointments', () =>
    axios.get('/api/clinics/appointments/').then((res) => res.data)
  );

  // Add new appointment
  const addAppointmentMutation = useMutation(
    (newAppointment: Partial<Appointment>) =>
      axios.post('/api/clinics/appointments/', newAppointment),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('clinic-appointments');
        enqueueSnackbar('Appointment scheduled successfully', {
          variant: 'success',
        });
        setNewAppointmentDialog(false);
      },
    }
  );

  // Add new service
  const addServiceMutation = useMutation(
    (data: { clinicId: number; service: any }) =>
      axios.post(`/api/clinics/${data.clinicId}/services/`, data.service),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('clinics');
        enqueueSnackbar('Service added successfully', {
          variant: 'success',
        });
        setNewServiceDialog(false);
      },
    }
  );

  const renderClinicsList = () => (
    <Paper sx={{ p: 2 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Clinics</Typography>
        <Button startIcon={<Add />} variant="contained">
          Add Clinic
        </Button>
      </Box>
      <List>
        {clinics?.map((clinic) => (
          <ListItem
            key={clinic.id}
            button
            onClick={() => setSelectedClinic(clinic)}
          >
            <ListItemAvatar>
              <Avatar>
                <LocalHospital />
              </Avatar>
            </ListItemAvatar>
            <ListItemText
              primary={clinic.name}
              secondary={`${clinic.specialization} - ${clinic.location}`}
            />
            <Chip
              label={`${clinic.doctors.length} Doctors`}
              color="primary"
              size="small"
            />
          </ListItem>
        ))}
      </List>
    </Paper>
  );

  const renderClinicDetails = () => (
    selectedClinic && (
      <Paper sx={{ p: 2 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">{selectedClinic.name}</Typography>
          <Box>
            <IconButton>
              <Edit />
            </IconButton>
            <IconButton>
              <LocationOn />
            </IconButton>
          </Box>
        </Box>

        <Grid container spacing={2} sx={{ mt: 1 }}>
          {/* Doctors */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Box
                  display="flex"
                  justifyContent="space-between"
                  alignItems="center"
                >
                  <Typography variant="h6">Doctors</Typography>
                  <Button startIcon={<Add />} size="small">
                    Add Doctor
                  </Button>
                </Box>
                <List dense>
                  {selectedClinic.doctors.map((doctor) => (
                    <ListItem key={doctor.id}>
                      <ListItemText
                        primary={doctor.name}
                        secondary={doctor.specialization}
                      />
                      <IconButton size="small">
                        <Event />
                      </IconButton>
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Services */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Box
                  display="flex"
                  justifyContent="space-between"
                  alignItems="center"
                >
                  <Typography variant="h6">Services</Typography>
                  <Button
                    startIcon={<Add />}
                    size="small"
                    onClick={() => setNewServiceDialog(true)}
                  >
                    Add Service
                  </Button>
                </Box>
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Service</TableCell>
                        <TableCell align="right">Price</TableCell>
                        <TableCell align="right">Duration</TableCell>
                        <TableCell />
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {selectedClinic.services.map((service) => (
                        <TableRow key={service.id}>
                          <TableCell>{service.name}</TableCell>
                          <TableCell align="right">
                            ${service.price}
                          </TableCell>
                          <TableCell align="right">
                            {service.duration} min
                          </TableCell>
                          <TableCell>
                            <IconButton size="small">
                              <Edit />
                            </IconButton>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Equipment */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Box
                  display="flex"
                  justifyContent="space-between"
                  alignItems="center"
                >
                  <Typography variant="h6">Equipment</Typography>
                  <Button startIcon={<Add />} size="small">
                    Add Equipment
                  </Button>
                </Box>
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Equipment</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Last Maintenance</TableCell>
                        <TableCell />
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {selectedClinic.equipment.map((item) => (
                        <TableRow key={item.id}>
                          <TableCell>{item.name}</TableCell>
                          <TableCell>
                            <Chip
                              label={item.status}
                              color={
                                item.status === 'operational'
                                  ? 'success'
                                  : item.status === 'maintenance'
                                  ? 'warning'
                                  : 'error'
                              }
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            {format(
                              new Date(item.lastMaintenance),
                              'MMM d, yyyy'
                            )}
                          </TableCell>
                          <TableCell>
                            <IconButton size="small">
                              <Edit />
                            </IconButton>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Paper>
    )
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
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Time</TableCell>
              <TableCell>Patient</TableCell>
              <TableCell>Doctor</TableCell>
              <TableCell>Service</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Payment</TableCell>
              <TableCell />
            </TableRow>
          </TableHead>
          <TableBody>
            {appointments?.map((appointment) => (
              <TableRow key={appointment.id}>
                <TableCell>
                  {format(new Date(appointment.dateTime), 'HH:mm')}
                </TableCell>
                <TableCell>{appointment.patientName}</TableCell>
                <TableCell>{appointment.doctorName}</TableCell>
                <TableCell>{appointment.service}</TableCell>
                <TableCell>
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
                </TableCell>
                <TableCell>
                  <Chip
                    label={`$${appointment.payment.amount} - ${appointment.payment.status}`}
                    color={
                      appointment.payment.status === 'paid'
                        ? 'success'
                        : 'warning'
                    }
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <IconButton size="small">
                    <Edit />
                  </IconButton>
                  <IconButton size="small">
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );

  if (loadingClinics || loadingAppointments) {
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
            <Typography variant="h4">Clinics Dashboard</Typography>
            <Button
              variant="contained"
              startIcon={<AttachMoney />}
              color="primary"
            >
              Financial Report
            </Button>
          </Box>
        </Grid>

        {/* Stats Cards */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Clinics
              </Typography>
              <Typography variant="h4">{clinics?.length || 0}</Typography>
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
                Available Doctors
              </Typography>
              <Typography variant="h4">
                {clinics?.reduce(
                  (total, clinic) => total + clinic.doctors.length,
                  0
                ) || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Today's Revenue
              </Typography>
              <Typography variant="h4">
                $
                {appointments
                  ?.filter(
                    (apt) =>
                      format(new Date(apt.dateTime), 'yyyy-MM-dd') ===
                        format(new Date(), 'yyyy-MM-dd') &&
                      apt.payment.status === 'paid'
                  )
                  .reduce((total, apt) => total + apt.payment.amount, 0)
                  .toFixed(2) || '0.00'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Main Content */}
        <Grid item xs={12} md={4}>
          {renderClinicsList()}
        </Grid>

        <Grid item xs={12} md={8}>
          {selectedClinic ? renderClinicDetails() : renderAppointments()}
        </Grid>
      </Grid>

      {/* New Service Dialog */}
      <Dialog
        open={newServiceDialog}
        onClose={() => setNewServiceDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Add New Service</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Service Name"
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Price"
                type="number"
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Duration (minutes)"
                type="number"
                variant="outlined"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setNewServiceDialog(false)}>Cancel</Button>
          <Button
            variant="contained"
            color="primary"
            disabled={addServiceMutation.isLoading}
          >
            Add Service
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ClinicsDashboard;
