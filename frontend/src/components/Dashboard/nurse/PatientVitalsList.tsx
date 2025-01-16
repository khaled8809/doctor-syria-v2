import React from 'react';
import {
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Box,
  Tooltip,
  Typography,
  Grid
} from '@mui/material';
import {
  Favorite,
  Thermostat,
  MonitorWeight,
  Opacity,
  Edit,
  Warning
} from '@mui/icons-material';

interface PatientVital {
  id: string;
  name: string;
  roomNumber: string;
  vitals: {
    heartRate: number;
    temperature: number;
    bloodPressure: string;
    oxygenSaturation: number;
  };
  lastUpdate: string;
  status: 'normal' | 'warning' | 'critical';
}

interface PatientVitalsListProps {
  patients: PatientVital[];
}

export const PatientVitalsList: React.FC<PatientVitalsListProps> = ({ patients }) => {
  const getStatusColor = (status: 'normal' | 'warning' | 'critical'): 'success' | 'warning' | 'error' => {
    switch (status) {
      case 'critical':
        return 'error';
      case 'warning':
        return 'warning';
      default:
        return 'success';
    }
  };

  return (
    <List>
      {patients.map((patient) => (
        <ListItem key={patient.id}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <ListItemText
                primary={patient.name}
                secondary={`Room ${patient.roomNumber}`}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Box display="flex" gap={2}>
                <Tooltip title="Heart Rate">
                  <Box display="flex" alignItems="center">
                    <Favorite color="error" />
                    <Typography variant="body2" sx={{ ml: 1 }}>
                      {patient.vitals.heartRate} bpm
                    </Typography>
                  </Box>
                </Tooltip>

                <Tooltip title="Temperature">
                  <Box display="flex" alignItems="center">
                    <Thermostat color="primary" />
                    <Typography variant="body2" sx={{ ml: 1 }}>
                      {patient.vitals.temperature}°C
                    </Typography>
                  </Box>
                </Tooltip>

                <Tooltip title="Blood Pressure">
                  <Box display="flex" alignItems="center">
                    <Opacity color="primary" />
                    <Typography variant="body2" sx={{ ml: 1 }}>
                      {patient.vitals.bloodPressure}
                    </Typography>
                  </Box>
                </Tooltip>

                <Tooltip title="Oxygen Saturation">
                  <Box display="flex" alignItems="center">
                    <MonitorWeight color="primary" />
                    <Typography variant="body2" sx={{ ml: 1 }}>
                      {patient.vitals.oxygenSaturation}%
                    </Typography>
                  </Box>
                </Tooltip>
              </Box>
            </Grid>
          </Grid>

          <ListItemSecondaryAction>
            <Box display="flex" alignItems="center" gap={1}>
              <Chip
                label={patient.status}
                color={getStatusColor(patient.status)}
                size="small"
              />
              <IconButton edge="end" aria-label="edit">
                <Edit />
              </IconButton>
              {patient.status === 'critical' && (
                <IconButton edge="end" aria-label="warning">
                  <Warning color="error" />
                </IconButton>
              )}
            </Box>
          </ListItemSecondaryAction>
        </ListItem>
      ))}
    </List>
  );
};

export default PatientVitalsList;
