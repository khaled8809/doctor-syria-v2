import { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
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
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Refresh as RefreshIcon,
  Check as CheckIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';

const deviceTypes = [
  { value: 'IMAGING', label: 'Imaging Device' },
  { value: 'LAB', label: 'Laboratory Device' },
  { value: 'VITAL_SIGNS', label: 'Vital Signs Monitor' },
  { value: 'OTHER', label: 'Other Device' },
];

interface Device {
  id: number;
  name: string;
  device_type: string;
  model_number: string;
  serial_number: string;
  status: string;
  last_maintenance: string;
  next_maintenance: string;
}

export default function Devices() {
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedDevice, setSelectedDevice] = useState<Device | null>(null);
  const queryClient = useQueryClient();

  const { data: devices, isLoading } = useQuery('devices', () =>
    axios.get('/api/medical-devices/').then((res) => res.data)
  );

  const addDeviceMutation = useMutation(
    (newDevice: Partial<Device>) =>
      axios.post('/api/medical-devices/', newDevice),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('devices');
        setOpenDialog(false);
      },
    }
  );

  const updateDeviceMutation = useMutation(
    (updatedDevice: Partial<Device>) =>
      axios.put(`/api/medical-devices/${selectedDevice?.id}/`, updatedDevice),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('devices');
        setOpenDialog(false);
      },
    }
  );

  const deleteDeviceMutation = useMutation(
    (id: number) => axios.delete(`/api/medical-devices/${id}/`),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('devices');
      },
    }
  );

  const handleAddDevice = () => {
    setSelectedDevice(null);
    setOpenDialog(true);
  };

  const handleEditDevice = (device: Device) => {
    setSelectedDevice(device);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedDevice(null);
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    const formData = new FormData(event.target as HTMLFormElement);
    const deviceData = Object.fromEntries(formData.entries());

    if (selectedDevice) {
      updateDeviceMutation.mutate(deviceData);
    } else {
      addDeviceMutation.mutate(deviceData);
    }
  };

  const getStatusChip = (status: string) => {
    const statusColors: { [key: string]: 'success' | 'error' | 'warning' | 'default' } = {
      ACTIVE: 'success',
      MAINTENANCE: 'warning',
      INACTIVE: 'error',
      UNKNOWN: 'default',
    };

    return (
      <Chip
        label={status}
        color={statusColors[status] || 'default'}
        size="small"
      />
    );
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Medical Devices</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleAddDevice}
        >
          Add Device
        </Button>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="h6">Device List</Typography>
                <IconButton onClick={() => queryClient.invalidateQueries('devices')}>
                  <RefreshIcon />
                </IconButton>
              </Box>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Name</TableCell>
                      <TableCell>Type</TableCell>
                      <TableCell>Model Number</TableCell>
                      <TableCell>Serial Number</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Last Maintenance</TableCell>
                      <TableCell>Next Maintenance</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {devices?.map((device: Device) => (
                      <TableRow key={device.id}>
                        <TableCell>{device.name}</TableCell>
                        <TableCell>{device.device_type}</TableCell>
                        <TableCell>{device.model_number}</TableCell>
                        <TableCell>{device.serial_number}</TableCell>
                        <TableCell>{getStatusChip(device.status)}</TableCell>
                        <TableCell>{new Date(device.last_maintenance).toLocaleDateString()}</TableCell>
                        <TableCell>{new Date(device.next_maintenance).toLocaleDateString()}</TableCell>
                        <TableCell>
                          <IconButton
                            size="small"
                            onClick={() => handleEditDevice(device)}
                          >
                            <EditIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => deleteDeviceMutation.mutate(device.id)}
                          >
                            <DeleteIcon />
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

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            {selectedDevice ? 'Edit Device' : 'Add New Device'}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Device Name"
                  name="name"
                  defaultValue={selectedDevice?.name}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth required>
                  <InputLabel>Device Type</InputLabel>
                  <Select
                    name="device_type"
                    defaultValue={selectedDevice?.device_type || ''}
                  >
                    {deviceTypes.map((type) => (
                      <MenuItem key={type.value} value={type.value}>
                        {type.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Model Number"
                  name="model_number"
                  defaultValue={selectedDevice?.model_number}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Serial Number"
                  name="serial_number"
                  defaultValue={selectedDevice?.serial_number}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Last Maintenance"
                  type="date"
                  name="last_maintenance"
                  defaultValue={selectedDevice?.last_maintenance?.split('T')[0]}
                  InputLabelProps={{ shrink: true }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Next Maintenance"
                  type="date"
                  name="next_maintenance"
                  defaultValue={selectedDevice?.next_maintenance?.split('T')[0]}
                  InputLabelProps={{ shrink: true }}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Cancel</Button>
            <Button
              type="submit"
              variant="contained"
              startIcon={selectedDevice ? <EditIcon /> : <AddIcon />}
            >
              {selectedDevice ? 'Update' : 'Add'} Device
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
}
