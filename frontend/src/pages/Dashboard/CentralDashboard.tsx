import React, { useState } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Tabs,
  Tab,
  IconButton,
  Button,
  Stack,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Sync as SyncIcon,
  LocalHospital as HospitalIcon,
  Store as StoreIcon,
  Person as PatientIcon,
  Warning as AlertIcon,
  Timeline as StatsIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { useSnackbar } from 'notistack';
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

interface SystemStatus {
  hospitals: {
    total: number;
    active: number;
    emergency_mode: number;
  };
  patients: {
    total: number;
    admitted: number;
    emergency: number;
  };
  inventory: {
    total_products: number;
    low_stock: number;
    out_of_stock: number;
  };
  orders: {
    pending: number;
    processing: number;
    urgent: number;
  };
  alerts: Array<{
    id: number;
    type: string;
    message: string;
    severity: 'error' | 'warning' | 'info';
    timestamp: string;
  }>;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const CentralDashboard = () => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [syncDialogOpen, setSyncDialogOpen] = useState(false);
  const [selectedHospital, setSelectedHospital] = useState<number | null>(null);

  const { enqueueSnackbar } = useSnackbar();
  const queryClient = useQueryClient();

  // Fetch system status
  const { data: systemStatus, isLoading } = useQuery<SystemStatus>(
    'system-status',
    () => axios.get('/api/system/status/').then((res) => res.data)
  );

  // Sync system mutation
  const syncSystemMutation = useMutation(
    () => axios.post('/api/system/sync/'),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('system-status');
        enqueueSnackbar('System synchronized successfully', {
          variant: 'success',
        });
        setSyncDialogOpen(false);
      },
      onError: (error: any) => {
        enqueueSnackbar(
          error.response?.data?.message || 'Error synchronizing system',
          { variant: 'error' }
        );
      },
    }
  );

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setSelectedTab(newValue);
  };

  const handleSync = () => {
    syncSystemMutation.mutate();
  };

  if (isLoading || !systemStatus) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100vh',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Stack
            direction="row"
            justifyContent="space-between"
            alignItems="center"
            sx={{ mb: 3 }}
          >
            <Typography variant="h4">Central Dashboard</Typography>
            <Button
              variant="contained"
              startIcon={<SyncIcon />}
              onClick={() => setSyncDialogOpen(true)}
            >
              Sync System
            </Button>
          </Stack>
        </Grid>

        {/* System Overview Cards */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active Hospitals
              </Typography>
              <Typography variant="h4">
                {systemStatus.hospitals.active}/{systemStatus.hospitals.total}
              </Typography>
              {systemStatus.hospitals.emergency_mode > 0 && (
                <Alert severity="warning" sx={{ mt: 1 }}>
                  {systemStatus.hospitals.emergency_mode} in emergency mode
                </Alert>
              )}
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
                {systemStatus.patients.admitted}
              </Typography>
              <Typography color="textSecondary">
                {systemStatus.patients.emergency} emergency cases
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Inventory Status
              </Typography>
              <Typography variant="h4">
                {systemStatus.inventory.total_products}
              </Typography>
              <Alert
                severity={
                  systemStatus.inventory.out_of_stock > 0 ? 'error' : 'info'
                }
                sx={{ mt: 1 }}
              >
                {systemStatus.inventory.out_of_stock} items out of stock
              </Alert>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Pending Orders
              </Typography>
              <Typography variant="h4">
                {systemStatus.orders.pending}
              </Typography>
              {systemStatus.orders.urgent > 0 && (
                <Alert severity="error" sx={{ mt: 1 }}>
                  {systemStatus.orders.urgent} urgent orders
                </Alert>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Tabs for different views */}
        <Grid item xs={12}>
          <Paper sx={{ width: '100%' }}>
            <Tabs
              value={selectedTab}
              onChange={handleTabChange}
              variant="fullWidth"
            >
              <Tab icon={<HospitalIcon />} label="Hospitals" />
              <Tab icon={<StoreIcon />} label="Inventory" />
              <Tab icon={<PatientIcon />} label="Patients" />
              <Tab icon={<AlertIcon />} label="Alerts" />
              <Tab icon={<StatsIcon />} label="Analytics" />
            </Tabs>
          </Paper>
        </Grid>

        {/* Tab Panels */}
        <Grid item xs={12}>
          {selectedTab === 0 && (
            <Paper sx={{ p: 2 }}>
              {/* Hospital Overview */}
              <Typography variant="h6" gutterBottom>
                Hospital Status
              </Typography>
              <Grid container spacing={2}>
                {/* Add hospital status components */}
              </Grid>
            </Paper>
          )}

          {selectedTab === 1 && (
            <Paper sx={{ p: 2 }}>
              {/* Inventory Overview */}
              <Typography variant="h6" gutterBottom>
                Inventory Status
              </Typography>
              <Grid container spacing={2}>
                {/* Add inventory status components */}
              </Grid>
            </Paper>
          )}

          {selectedTab === 2 && (
            <Paper sx={{ p: 2 }}>
              {/* Patient Overview */}
              <Typography variant="h6" gutterBottom>
                Patient Statistics
              </Typography>
              <Grid container spacing={2}>
                {/* Add patient statistics components */}
              </Grid>
            </Paper>
          )}

          {selectedTab === 3 && (
            <Paper sx={{ p: 2 }}>
              {/* System Alerts */}
              <Typography variant="h6" gutterBottom>
                System Alerts
              </Typography>
              <Stack spacing={2}>
                {systemStatus.alerts.map((alert) => (
                  <Alert key={alert.id} severity={alert.severity}>
                    {alert.message}
                  </Alert>
                ))}
              </Stack>
            </Paper>
          )}

          {selectedTab === 4 && (
            <Paper sx={{ p: 2 }}>
              {/* Analytics */}
              <Typography variant="h6" gutterBottom>
                System Analytics
              </Typography>
              <Grid container spacing={2}>
                {/* Add analytics components */}
              </Grid>
            </Paper>
          )}
        </Grid>
      </Grid>

      {/* Sync Dialog */}
      <Dialog
        open={syncDialogOpen}
        onClose={() => setSyncDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Synchronize System</DialogTitle>
        <DialogContent>
          <Typography>
            This will synchronize all system components including:
          </Typography>
          <ul>
            <li>Hospital data and bed availability</li>
            <li>Inventory levels and orders</li>
            <li>Patient records and admissions</li>
            <li>Emergency cases and transfers</li>
          </ul>
          <Typography color="error">
            Note: This process may take a few minutes.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSyncDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleSync}
            disabled={syncSystemMutation.isLoading}
          >
            {syncSystemMutation.isLoading ? (
              <CircularProgress size={24} />
            ) : (
              'Sync Now'
            )}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default CentralDashboard;
