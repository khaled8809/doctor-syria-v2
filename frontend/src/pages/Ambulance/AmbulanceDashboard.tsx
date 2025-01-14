import React, { useState } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Button,
  IconButton,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import {
  LocalHospital,
  LocationOn,
  Speed,
  Timer,
  Warning,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { useSnackbar } from 'notistack';
import {
  GoogleMap,
  useLoadScript,
  Marker,
  InfoWindow,
} from '@react-google-maps/api';

interface Ambulance {
  id: string;
  status: 'available' | 'dispatched' | 'returning' | 'maintenance';
  location: {
    latitude: number;
    longitude: number;
  };
  currentTask?: {
    id: string;
    type: string;
    priority: string;
    destination: {
      latitude: number;
      longitude: number;
    };
    eta: string;
  };
  lastMaintenance: string;
  crew: {
    driver: string;
    paramedic: string;
    nurse?: string;
  };
}

const AmbulanceDashboard = () => {
  const [selectedAmbulance, setSelectedAmbulance] = useState<Ambulance | null>(
    null
  );
  const [dispatchDialogOpen, setDispatchDialogOpen] = useState(false);
  const [mapCenter, setMapCenter] = useState({ lat: 33.5138, lng: 36.2765 });
  const { enqueueSnackbar } = useSnackbar();
  const queryClient = useQueryClient();

  const { isLoaded } = useLoadScript({
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY || '',
  });

  // Fetch ambulances data
  const { data: ambulances, isLoading } = useQuery<Ambulance[]>(
    'ambulances',
    () => axios.get('/api/ambulances/').then((res) => res.data)
  );

  // Dispatch ambulance mutation
  const dispatchMutation = useMutation(
    (data: { ambulanceId: string; destination: any; priority: string }) =>
      axios.post('/api/ambulances/dispatch/', data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('ambulances');
        enqueueSnackbar('Ambulance dispatched successfully', {
          variant: 'success',
        });
        setDispatchDialogOpen(false);
      },
      onError: (error: any) => {
        enqueueSnackbar(error.response?.data?.message || 'Error dispatching ambulance', {
          variant: 'error',
        });
      },
    }
  );

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'available':
        return 'success';
      case 'dispatched':
        return 'error';
      case 'returning':
        return 'warning';
      case 'maintenance':
        return 'default';
      default:
        return 'default';
    }
  };

  const handleDispatch = (ambulance: Ambulance) => {
    setSelectedAmbulance(ambulance);
    setDispatchDialogOpen(true);
  };

  if (!isLoaded) return <div>Loading maps...</div>;
  if (isLoading) return <div>Loading ambulances...</div>;

  return (
    <Box sx={{ p: 3 }}>
      <Grid container spacing={3}>
        {/* Header */}
        <Grid item xs={12}>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h4">Ambulance Dashboard</Typography>
            <Button
              variant="contained"
              startIcon={<Warning />}
              color="error"
              onClick={() => setDispatchDialogOpen(true)}
            >
              Emergency Dispatch
            </Button>
          </Box>
        </Grid>

        {/* Stats Cards */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Available Ambulances
              </Typography>
              <Typography variant="h4">
                {ambulances?.filter((a) => a.status === 'available').length || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active Dispatches
              </Typography>
              <Typography variant="h4">
                {ambulances?.filter((a) => a.status === 'dispatched').length || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Average Response Time
              </Typography>
              <Typography variant="h4">8.5 min</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                In Maintenance
              </Typography>
              <Typography variant="h4">
                {ambulances?.filter((a) => a.status === 'maintenance').length || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Map */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, height: 500 }}>
            <GoogleMap
              zoom={12}
              center={mapCenter}
              mapContainerStyle={{ width: '100%', height: '100%' }}
            >
              {ambulances?.map((ambulance) => (
                <Marker
                  key={ambulance.id}
                  position={{
                    lat: ambulance.location.latitude,
                    lng: ambulance.location.longitude,
                  }}
                  onClick={() => setSelectedAmbulance(ambulance)}
                  icon={{
                    url: `/ambulance-${ambulance.status}.png`,
                    scaledSize: new window.google.maps.Size(30, 30),
                  }}
                />
              ))}

              {selectedAmbulance && (
                <InfoWindow
                  position={{
                    lat: selectedAmbulance.location.latitude,
                    lng: selectedAmbulance.location.longitude,
                  }}
                  onCloseClick={() => setSelectedAmbulance(null)}
                >
                  <div>
                    <Typography variant="subtitle1">
                      Ambulance {selectedAmbulance.id}
                    </Typography>
                    <Typography variant="body2">
                      Status:{' '}
                      <Chip
                        size="small"
                        label={selectedAmbulance.status}
                        color={getStatusColor(selectedAmbulance.status) as any}
                      />
                    </Typography>
                    {selectedAmbulance.currentTask && (
                      <>
                        <Typography variant="body2">
                          Task: {selectedAmbulance.currentTask.type}
                        </Typography>
                        <Typography variant="body2">
                          ETA: {selectedAmbulance.currentTask.eta}
                        </Typography>
                      </>
                    )}
                  </div>
                </InfoWindow>
              )}
            </GoogleMap>
          </Paper>
        </Grid>

        {/* Ambulance List */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: 500, overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>
              Ambulance Status
            </Typography>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Location</TableCell>
                  <TableCell>Action</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {ambulances?.map((ambulance) => (
                  <TableRow key={ambulance.id}>
                    <TableCell>{ambulance.id}</TableCell>
                    <TableCell>
                      <Chip
                        size="small"
                        label={ambulance.status}
                        color={getStatusColor(ambulance.status) as any}
                      />
                    </TableCell>
                    <TableCell>
                      <IconButton
                        size="small"
                        onClick={() => {
                          setMapCenter({
                            lat: ambulance.location.latitude,
                            lng: ambulance.location.longitude,
                          });
                          setSelectedAmbulance(ambulance);
                        }}
                      >
                        <LocationOn />
                      </IconButton>
                    </TableCell>
                    <TableCell>
                      <Button
                        size="small"
                        variant="contained"
                        disabled={ambulance.status !== 'available'}
                        onClick={() => handleDispatch(ambulance)}
                      >
                        Dispatch
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Paper>
        </Grid>
      </Grid>

      {/* Dispatch Dialog */}
      <Dialog
        open={dispatchDialogOpen}
        onClose={() => setDispatchDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Dispatch Ambulance</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Destination Address"
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Priority"
                select
                SelectProps={{
                  native: true,
                }}
                variant="outlined"
              >
                <option value="high">High Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="low">Low Priority</option>
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={4}
                label="Additional Notes"
                variant="outlined"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDispatchDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            color="primary"
            disabled={dispatchMutation.isLoading}
          >
            Dispatch Now
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AmbulanceDashboard;
