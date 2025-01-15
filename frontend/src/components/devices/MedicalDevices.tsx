import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Switch,
  FormControlLabel,
  Alert,
  CircularProgress,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  DevicesOther as DevicesIcon,
  Favorite as HeartIcon,
  Timeline as TimelineIcon,
  Sync as SyncIcon,
  Warning as WarningIcon,
  Add as AddIcon,
  Settings as SettingsIcon,
  Delete as DeleteIcon,
  Notifications as NotificationsIcon,
} from '@mui/icons-material';
import { Line } from 'react-chartjs-2';
import { useTranslation } from 'react-i18next';

interface MedicalDevice {
  id: string;
  name: string;
  type: string;
  status: 'connected' | 'disconnected' | 'error';
  lastSync: string;
  batteryLevel: number;
  readings: {
    timestamp: string;
    value: number;
  }[];
  thresholds: {
    min: number;
    max: number;
  };
}

interface DeviceReading {
  id: string;
  deviceId: string;
  timestamp: string;
  type: string;
  value: number;
  unit: string;
  status: 'normal' | 'warning' | 'critical';
}

const MedicalDevices: React.FC = () => {
  const { t } = useTranslation();
  const [devices, setDevices] = useState<MedicalDevice[]>([]);
  const [readings, setReadings] = useState<DeviceReading[]>([]);
  const [selectedDevice, setSelectedDevice] = useState<MedicalDevice | null>(null);
  const [showAddDevice, setShowAddDevice] = useState(false);
  const [loading, setLoading] = useState(false);
  const [syncingDevice, setSyncingDevice] = useState<string | null>(null);

  useEffect(() => {
    // Fetch devices and readings
    fetchDevicesData();
  }, []);

  const fetchDevicesData = async () => {
    // This would be replaced with actual API calls
    const mockDevices: MedicalDevice[] = [
      {
        id: '1',
        name: 'جهاز قياس ضغط الدم',
        type: 'blood_pressure',
        status: 'connected',
        lastSync: '2025-01-08T14:30:00',
        batteryLevel: 85,
        readings: [
          { timestamp: '2025-01-08T14:00:00', value: 120 },
          { timestamp: '2025-01-08T14:30:00', value: 118 },
        ],
        thresholds: { min: 90, max: 140 },
      },
      {
        id: '2',
        name: 'جهاز قياس السكر',
        type: 'glucose',
        status: 'connected',
        lastSync: '2025-01-08T15:00:00',
        batteryLevel: 92,
        readings: [
          { timestamp: '2025-01-08T14:00:00', value: 110 },
          { timestamp: '2025-01-08T15:00:00', value: 115 },
        ],
        thresholds: { min: 70, max: 180 },
      },
    ];

    const mockReadings: DeviceReading[] = [
      {
        id: '1',
        deviceId: '1',
        timestamp: '2025-01-08T14:30:00',
        type: 'blood_pressure',
        value: 118,
        unit: 'mmHg',
        status: 'normal',
      },
      {
        id: '2',
        deviceId: '2',
        timestamp: '2025-01-08T15:00:00',
        type: 'glucose',
        value: 115,
        unit: 'mg/dL',
        status: 'normal',
      },
    ];

    setDevices(mockDevices);
    setReadings(mockReadings);
  };

  const syncDevice = async (deviceId: string) => {
    setSyncingDevice(deviceId);
    try {
      // Simulate device sync
      await new Promise(resolve => setTimeout(resolve, 2000));
      // Update last sync time
      setDevices(prev =>
        prev.map(device =>
          device.id === deviceId
            ? { ...device, lastSync: new Date().toISOString() }
            : device
        )
      );
    } catch (error) {
      console.error('Error syncing device:', error);
    } finally {
      setSyncingDevice(null);
    }
  };

  const renderDevicesList = () => (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">{t('devices.connectedDevices')}</Typography>
        <Button
          startIcon={<AddIcon />}
          variant="contained"
          onClick={() => setShowAddDevice(true)}
        >
          {t('devices.addDevice')}
        </Button>
      </Box>
      <List>
        {devices.map(device => (
          <ListItem
            key={device.id}
            button
            onClick={() => setSelectedDevice(device)}
          >
            <ListItemIcon>
              <DevicesIcon />
            </ListItemIcon>
            <ListItemText
              primary={
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  {device.name}
                  <Chip
                    label={t(`devices.status.${device.status}`)}
                    color={
                      device.status === 'connected'
                        ? 'success'
                        : device.status === 'error'
                        ? 'error'
                        : 'warning'
                    }
                    size="small"
                    sx={{ ml: 1 }}
                  />
                </Box>
              }
              secondary={`${t('devices.lastSync')}: ${new Date(device.lastSync).toLocaleString()}`}
            />
            <ListItemSecondaryAction>
              <IconButton
                onClick={(e) => {
                  e.stopPropagation();
                  syncDevice(device.id);
                }}
                disabled={syncingDevice === device.id}
              >
                {syncingDevice === device.id ? (
                  <CircularProgress size={24} />
                ) : (
                  <SyncIcon />
                )}
              </IconButton>
              <IconButton onClick={(e) => e.stopPropagation()}>
                <SettingsIcon />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>
    </Paper>
  );

  const renderDeviceDetails = () => {
    if (!selectedDevice) return null;

    const deviceReadings = readings.filter(r => r.deviceId === selectedDevice.id);

    return (
      <Dialog
        open={!!selectedDevice}
        onClose={() => setSelectedDevice(null)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            {selectedDevice.name}
            <Box>
              <IconButton size="small">
                <SettingsIcon />
              </IconButton>
              <IconButton size="small" onClick={() => setSelectedDevice(null)}>
                <DeleteIcon />
              </IconButton>
            </Box>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {t('devices.latestReadings')}
                  </Typography>
                  <Line
                    data={{
                      labels: selectedDevice.readings.map(r =>
                        new Date(r.timestamp).toLocaleTimeString()
                      ),
                      datasets: [
                        {
                          label: t(`devices.types.${selectedDevice.type}`),
                          data: selectedDevice.readings.map(r => r.value),
                          borderColor: 'rgb(75, 192, 192)',
                          tension: 0.1,
                        },
                      ],
                    }}
                    options={{
                      responsive: true,
                      plugins: {
                        legend: {
                          position: 'top',
                        },
                      },
                      scales: {
                        y: {
                          beginAtZero: false,
                        },
                      },
                    }}
                  />
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Card>
                <CardContent>
                  <Typography variant="subtitle1" gutterBottom>
                    {t('devices.deviceInfo')}
                  </Typography>
                  <List>
                    <ListItem>
                      <ListItemText
                        primary={t('devices.status')}
                        secondary={t(`devices.status.${selectedDevice.status}`)}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary={t('devices.batteryLevel')}
                        secondary={
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <LinearProgress
                              variant="determinate"
                              value={selectedDevice.batteryLevel}
                              sx={{ flexGrow: 1, mr: 1 }}
                            />
                            {selectedDevice.batteryLevel}%
                          </Box>
                        }
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary={t('devices.lastSync')}
                        secondary={new Date(selectedDevice.lastSync).toLocaleString()}
                      />
                    </ListItem>
                  </List>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Card>
                <CardContent>
                  <Typography variant="subtitle1" gutterBottom>
                    {t('devices.thresholds')}
                  </Typography>
                  <List>
                    <ListItem>
                      <ListItemText
                        primary={t('devices.minThreshold')}
                        secondary={selectedDevice.thresholds.min}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary={t('devices.maxThreshold')}
                        secondary={selectedDevice.thresholds.max}
                      />
                    </ListItem>
                  </List>
                </CardContent>
                <CardActions>
                  <Button size="small" startIcon={<SettingsIcon />}>
                    {t('devices.adjustThresholds')}
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          </Grid>
        </DialogContent>
      </Dialog>
    );
  };

  const renderAddDeviceDialog = () => (
    <Dialog
      open={showAddDevice}
      onClose={() => setShowAddDevice(false)}
      maxWidth="sm"
      fullWidth
    >
      <DialogTitle>{t('devices.addDevice')}</DialogTitle>
      <DialogContent>
        <Alert severity="info" sx={{ mb: 2 }}>
          {t('devices.pairingInstructions')}
        </Alert>
        <TextField
          fullWidth
          label={t('devices.deviceName')}
          margin="normal"
        />
        <TextField
          fullWidth
          label={t('devices.deviceType')}
          select
          margin="normal"
        >
          <MenuItem value="blood_pressure">
            {t('devices.types.blood_pressure')}
          </MenuItem>
          <MenuItem value="glucose">
            {t('devices.types.glucose')}
          </MenuItem>
          <MenuItem value="heart_rate">
            {t('devices.types.heart_rate')}
          </MenuItem>
        </TextField>
        <FormControlLabel
          control={<Switch />}
          label={t('devices.enableNotifications')}
          sx={{ mt: 2 }}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setShowAddDevice(false)}>
          {t('common.cancel')}
        </Button>
        <Button
          variant="contained"
          onClick={() => {
            // Add device logic would go here
            setShowAddDevice(false);
          }}
        >
          {t('devices.startPairing')}
        </Button>
      </DialogActions>
    </Dialog>
  );

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          {t('devices.title')}
        </Typography>

        {renderDevicesList()}
        {renderDeviceDetails()}
        {renderAddDeviceDialog()}
      </Box>
    </Container>
  );
};

export default MedicalDevices;
