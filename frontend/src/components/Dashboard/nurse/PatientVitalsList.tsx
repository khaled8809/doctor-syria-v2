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
  Typography
} from '@mui/material';
import {
  Favorite,
  DeviceThermometerIcon,
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
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'critical':
        return 'error';
      case 'warning':
        return 'warning';
      default:
        return 'success';
    }
  };

  const getVitalColor = (value: number, type: string) => {
    switch (type) {
      case 'heartRate':
        return value < 60 || value > 100 ? 'error.main' : 'success.main';
      case 'temperature':
        return value < 36 || value > 38 ? 'error.main' : 'success.main';
      case 'oxygenSaturation':
        return value < 95 ? 'error.main' : 'success.main';
      default:
        return 'text.primary';
    }
  };

  return (
    <List>
      {patients.map((patient) => (
        <ListItem
          key={patient.id}
          sx={{
            mb: 1,
            border: 1,
            borderColor: 'divider',
            borderRadius: 1,
            '&:hover': {
              backgroundColor: 'action.hover',
            },
          }}
        >
          <ListItemText
            primary={
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Typography variant="subtitle1">{patient.name}</Typography>
                <Chip
                  size="small"
                  label={`غرفة ${patient.roomNumber}`}
                  color="primary"
                  variant="outlined"
                />
                {patient.status !== 'normal' && (
                  <Tooltip title="حالة تحتاج انتباه">
                    <Warning color="error" />
                  </Tooltip>
                )}
              </Box>
            }
            secondary={
              <Box sx={{ mt: 1 }}>
                <Grid container spacing={2}>
                  <Grid item xs={3}>
                    <Tooltip title="معدل ضربات القلب">
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <Favorite sx={{ color: getVitalColor(patient.vitals.heartRate, 'heartRate') }} />
                        <Typography
                          variant="body2"
                          color={getVitalColor(patient.vitals.heartRate, 'heartRate')}
                        >
                          {patient.vitals.heartRate} bpm
                        </Typography>
                      </Box>
                    </Tooltip>
                  </Grid>
                  <Grid item xs={3}>
                    <Tooltip title="درجة الحرارة">
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <DeviceThermometerIcon sx={{ color: getVitalColor(patient.vitals.temperature, 'temperature') }} />
                        <Typography
                          variant="body2"
                          color={getVitalColor(patient.vitals.temperature, 'temperature')}
                        >
                          {patient.vitals.temperature}°C
                        </Typography>
                      </Box>
                    </Tooltip>
                  </Grid>
                  <Grid item xs={3}>
                    <Tooltip title="ضغط الدم">
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <MonitorWeight color="primary" />
                        <Typography variant="body2">
                          {patient.vitals.bloodPressure}
                        </Typography>
                      </Box>
                    </Tooltip>
                  </Grid>
                  <Grid item xs={3}>
                    <Tooltip title="تشبع الأكسجين">
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <Opacity sx={{ color: getVitalColor(patient.vitals.oxygenSaturation, 'oxygenSaturation') }} />
                        <Typography
                          variant="body2"
                          color={getVitalColor(patient.vitals.oxygenSaturation, 'oxygenSaturation')}
                        >
                          {patient.vitals.oxygenSaturation}%
                        </Typography>
                      </Box>
                    </Tooltip>
                  </Grid>
                </Grid>
                <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                  آخر تحديث: {patient.lastUpdate}
                </Typography>
              </Box>
            }
          />
          <ListItemSecondaryAction>
            <IconButton edge="end" aria-label="تحديث">
              <Edit />
            </IconButton>
          </ListItemSecondaryAction>
        </ListItem>
      ))}
    </List>
  );
};

export default PatientVitalsList;
