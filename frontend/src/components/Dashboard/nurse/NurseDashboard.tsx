import React from 'react';
import { Grid, Paper, Typography, Box, Chip, Button } from '@mui/material';
import {
  AccessTime,
  Assignment,
  Favorite,
  NotificationsActive
} from '@mui/icons-material';
import { PatientVitalsList } from './PatientVitalsList';
import { TaskSchedule } from './TaskSchedule';
import { MedicationSchedule } from './MedicationSchedule';
import { useNurseStats } from '../../../hooks/useNurseStats';
import { Patient, Task, Medication, PatientVital } from '../../../types/common';

const NurseDashboard: React.FC = () => {
  const { stats, tasks, patients, medications, loading } = useNurseStats();

  if (loading) return <div>Loading...</div>;

  // Convert Patient[] to PatientVital[]
  const patientVitals: PatientVital[] = patients.map(patient => ({
    ...patient,
    status: getPatientStatus(patient)
  }));

  // Helper function to determine patient status based on vitals
  function getPatientStatus(patient: Patient): 'normal' | 'warning' | 'critical' {
    if (!patient.vitals) return 'normal';

    const { heartRate, temperature, oxygenSaturation } = patient.vitals;

    if (
      heartRate > 100 || heartRate < 60 ||
      temperature > 38.5 || temperature < 36 ||
      oxygenSaturation < 92
    ) {
      return 'critical';
    }

    if (
      heartRate > 90 || heartRate < 65 ||
      temperature > 37.8 || temperature < 36.5 ||
      oxygenSaturation < 95
    ) {
      return 'warning';
    }

    return 'normal';
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Nurse Dashboard</Typography>
        <Box>
          <Chip
            icon={<AccessTime />}
            label={`Shift: ${stats.currentShift}`}
            color="primary"
            sx={{ mr: 1 }}
          />
          <Button
            variant="contained"
            color="primary"
            startIcon={<NotificationsActive />}
          >
            Emergency Alert
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Current Ward Status */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Current Ward Status
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6} sm={3}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="primary">
                    {stats.totalPatients}
                  </Typography>
                  <Typography variant="body2">Total Patients</Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="error">
                    {stats.criticalCases}
                  </Typography>
                  <Typography variant="body2">Critical Cases</Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="warning.main">
                    {stats.pendingTasks}
                  </Typography>
                  <Typography variant="body2">Pending Tasks</Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="success.main">
                    {stats.completedTasks}
                  </Typography>
                  <Typography variant="body2">Completed Tasks</Typography>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Grid container spacing={1}>
              <Grid item xs={6}>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<Assignment />}
                  sx={{ mb: 1 }}
                >
                  Record Vitals
                </Button>
              </Grid>
              <Grid item xs={6}>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<Favorite />}
                  sx={{ mb: 1 }}
                >
                  Request Doctor
                </Button>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Patient Vitals */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '400px', overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>
              Patient Vitals
            </Typography>
            <PatientVitalsList patients={patientVitals} />
          </Paper>
        </Grid>

        {/* Task Schedule */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '400px', overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>
              Task Schedule
            </Typography>
            <TaskSchedule tasks={tasks} />
          </Paper>
        </Grid>

        {/* Medication Schedule */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Medication Schedule
            </Typography>
            <MedicationSchedule medications={medications} />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default NurseDashboard;
