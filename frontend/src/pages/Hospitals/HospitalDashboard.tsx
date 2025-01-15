import React, { useState } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Button,
  IconButton,
  Stack,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
} from '@mui/material';
import {
  LocalHospital as HospitalIcon,
  Person as PatientIcon,
  Event as AdmissionIcon,
  LocalShipping as TransferIcon,
  Warning as EmergencyIcon,
  Bed as BedIcon,
  MeetingRoom as RoomIcon,
  Timeline as StatsIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { useSnackbar } from 'notistack';
import { format } from 'date-fns';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

interface Hospital {
  id: number;
  name: string;
  city: string;
  type: string;
  bed_capacity: number;
  available_beds: number;
  icu_units: number;
  operating_rooms: number;
}

interface Department {
  id: number;
  name: string;
  specialty: string;
  capacity: number;
  available_beds: number;
}

interface Doctor {
  id: number;
  name: string;
  specialty: string;
  is_active: boolean;
}

interface Admission {
  id: number;
  patient_name: string;
  admission_date: string;
  status: string;
  department: string;
  doctor_name: string;
}

interface EmergencyCase {
  id: number;
  patient_name: string;
  arrival_date: string;
  priority: string;
  condition: string;
  outcome: string;
}

interface Statistics {
  total_admissions: number;
  current_patients: number;
  discharges: number;
  transfers: number;
  deaths: number;
  emergency_cases: {
    total: number;
    by_priority: {
      critical: number;
      urgent: number;
      non_urgent: number;
    };
    outcomes: {
      admitted: number;
      discharged: number;
      transferred: number;
      deceased: number;
    };
  };
  bed_utilization: number;
  average_stay: number;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const HospitalDashboard = () => {
  const [selectedHospital, setSelectedHospital] = useState<number | null>(null);
  const [admissionDialogOpen, setAdmissionDialogOpen] = useState(false);
  const [transferDialogOpen, setTransferDialogOpen] = useState(false);
  const [emergencyDialogOpen, setEmergencyDialogOpen] = useState(false);

  const { enqueueSnackbar } = useSnackbar();
  const queryClient = useQueryClient();

  // Fetch hospital data
  const { data: hospitals } = useQuery<Hospital[]>('hospitals', () =>
    axios.get('/api/hospitals/').then((res) => res.data)
  );

  // Fetch statistics for selected hospital
  const { data: statistics } = useQuery<Statistics>(
    ['hospital-statistics', selectedHospital],
    () =>
      axios
        .get(`/api/hospitals/${selectedHospital}/statistics/`)
        .then((res) => res.data),
    {
      enabled: !!selectedHospital,
    }
  );

  // Fetch recent admissions
  const { data: recentAdmissions } = useQuery<Admission[]>(
    ['recent-admissions', selectedHospital],
    () =>
      axios
        .get(`/api/hospitals/${selectedHospital}/admissions/recent/`)
        .then((res) => res.data),
    {
      enabled: !!selectedHospital,
    }
  );

  // Fetch emergency cases
  const { data: emergencyCases } = useQuery<EmergencyCase[]>(
    ['emergency-cases', selectedHospital],
    () =>
      axios
        .get(`/api/hospitals/${selectedHospital}/emergency-cases/`)
        .then((res) => res.data),
    {
      enabled: !!selectedHospital,
    }
  );

  const handleHospitalChange = (event: any) => {
    setSelectedHospital(event.target.value);
  };

  if (!hospitals) {
    return <div>Loading...</div>;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <FormControl fullWidth>
              <InputLabel>Select Hospital</InputLabel>
              <Select
                value={selectedHospital || ''}
                onChange={handleHospitalChange}
                label="Select Hospital"
              >
                {hospitals.map((hospital) => (
                  <MenuItem key={hospital.id} value={hospital.id}>
                    {hospital.name} - {hospital.city}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Paper>
        </Grid>

        {selectedHospital && statistics && (
          <>
            {/* Statistics Cards */}
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Total Admissions
                  </Typography>
                  <Typography variant="h4">
                    {statistics.total_admissions}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Current Patients
                  </Typography>
                  <Typography variant="h4">
                    {statistics.current_patients}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Bed Utilization
                  </Typography>
                  <Typography variant="h4">
                    {statistics.bed_utilization.toFixed(1)}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={statistics.bed_utilization}
                    sx={{ mt: 1 }}
                  />
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Emergency Cases
                  </Typography>
                  <Typography variant="h4">
                    {statistics.emergency_cases.total}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* Charts */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Emergency Cases by Priority
                </Typography>
                <PieChart width={400} height={300}>
                  <Pie
                    data={[
                      {
                        name: 'Critical',
                        value: statistics.emergency_cases.by_priority.critical,
                      },
                      {
                        name: 'Urgent',
                        value: statistics.emergency_cases.by_priority.urgent,
                      },
                      {
                        name: 'Non-Urgent',
                        value: statistics.emergency_cases.by_priority.non_urgent,
                      },
                    ]}
                    cx={200}
                    cy={150}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label
                  >
                    {COLORS.map((color, index) => (
                      <Cell key={`cell-${index}`} fill={color} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </Paper>
            </Grid>

            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Patient Outcomes
                </Typography>
                <BarChart
                  width={400}
                  height={300}
                  data={[
                    {
                      name: 'Discharged',
                      value: statistics.discharges,
                    },
                    {
                      name: 'Transferred',
                      value: statistics.transfers,
                    },
                    {
                      name: 'Deceased',
                      value: statistics.deaths,
                    },
                  ]}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="value" fill="#8884d8" />
                </BarChart>
              </Paper>
            </Grid>

            {/* Recent Admissions */}
            <Grid item xs={12}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Recent Admissions
                </Typography>
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Patient</TableCell>
                        <TableCell>Date</TableCell>
                        <TableCell>Department</TableCell>
                        <TableCell>Doctor</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {recentAdmissions?.map((admission) => (
                        <TableRow key={admission.id}>
                          <TableCell>{admission.patient_name}</TableCell>
                          <TableCell>
                            {format(
                              new Date(admission.admission_date),
                              'MMM d, yyyy'
                            )}
                          </TableCell>
                          <TableCell>{admission.department}</TableCell>
                          <TableCell>{admission.doctor_name}</TableCell>
                          <TableCell>
                            <Chip
                              label={admission.status}
                              color={
                                admission.status === 'ADMITTED'
                                  ? 'primary'
                                  : admission.status === 'DISCHARGED'
                                  ? 'success'
                                  : 'default'
                              }
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <IconButton
                              size="small"
                              onClick={() => {
                                // Handle view details
                              }}
                            >
                              <StatsIcon />
                            </IconButton>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Paper>
            </Grid>

            {/* Emergency Cases */}
            <Grid item xs={12}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Emergency Cases
                </Typography>
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Patient</TableCell>
                        <TableCell>Arrival</TableCell>
                        <TableCell>Priority</TableCell>
                        <TableCell>Condition</TableCell>
                        <TableCell>Outcome</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {emergencyCases?.map((emergency) => (
                        <TableRow key={emergency.id}>
                          <TableCell>{emergency.patient_name}</TableCell>
                          <TableCell>
                            {format(
                              new Date(emergency.arrival_date),
                              'MMM d, yyyy HH:mm'
                            )}
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={emergency.priority}
                              color={
                                emergency.priority === 'CRITICAL'
                                  ? 'error'
                                  : emergency.priority === 'URGENT'
                                  ? 'warning'
                                  : 'info'
                              }
                              size="small"
                            />
                          </TableCell>
                          <TableCell>{emergency.condition}</TableCell>
                          <TableCell>
                            <Chip
                              label={emergency.outcome}
                              color={
                                emergency.outcome === 'ADMITTED'
                                  ? 'primary'
                                  : emergency.outcome === 'DISCHARGED'
                                  ? 'success'
                                  : 'default'
                              }
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <IconButton
                              size="small"
                              onClick={() => {
                                // Handle view details
                              }}
                            >
                              <StatsIcon />
                            </IconButton>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Paper>
            </Grid>

            {/* Action Buttons */}
            <Grid item xs={12}>
              <Stack direction="row" spacing={2}>
                <Button
                  variant="contained"
                  startIcon={<AdmissionIcon />}
                  onClick={() => setAdmissionDialogOpen(true)}
                >
                  New Admission
                </Button>
                <Button
                  variant="contained"
                  startIcon={<TransferIcon />}
                  onClick={() => setTransferDialogOpen(true)}
                >
                  Transfer Patient
                </Button>
                <Button
                  variant="contained"
                  color="error"
                  startIcon={<EmergencyIcon />}
                  onClick={() => setEmergencyDialogOpen(true)}
                >
                  Register Emergency
                </Button>
              </Stack>
            </Grid>
          </>

        )}
      </Grid>

      {/* Dialogs for actions */}
      {/* Add implementation for admission, transfer, and emergency dialogs */}
    </Box>
  );
};

export default HospitalDashboard;
