import React, { useState } from 'react';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  IconButton,
  Button,
  Typography,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Grid,
  Card,
  CardContent,
  Stack,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Thermostat as ThermostatIcon,
  Inventory as InventoryIcon,
  Person as PersonIcon,
  WaterDrop as HumidityIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { useSnackbar } from 'notistack';

interface Warehouse {
  id: number;
  name: string;
  warehouse_type: string;
  location: string;
  capacity: number;
  temperature: number;
  humidity: number;
  manager: {
    id: number;
    name: string;
  };
  is_active: boolean;
}

interface WarehouseFormData {
  name: string;
  warehouse_type: string;
  location: string;
  capacity: number;
  temperature: number;
  humidity: number;
  manager_id: number;
}

const WAREHOUSE_TYPES = [
  { value: 'MEDICAL_SUPPLIES', label: 'Medical Supplies' },
  { value: 'MEDICATIONS', label: 'Medications' },
  { value: 'EQUIPMENT', label: 'Medical Equipment' },
  { value: 'GENERAL', label: 'General Storage' },
];

const Warehouses = () => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedWarehouse, setSelectedWarehouse] = useState<Warehouse | null>(null);
  const [formData, setFormData] = useState<WarehouseFormData>({
    name: '',
    warehouse_type: '',
    location: '',
    capacity: 0,
    temperature: 20,
    humidity: 50,
    manager_id: 0,
  });

  const queryClient = useQueryClient();
  const { enqueueSnackbar } = useSnackbar();

  // Fetch warehouses
  const { data: warehouses, isLoading } = useQuery('warehouses', () =>
    axios.get('/api/inventory/warehouses/').then((res) => res.data)
  );

  // Fetch users for manager selection
  const { data: users } = useQuery('users', () =>
    axios.get('/api/users/').then((res) => res.data)
  );

  // Fetch warehouse statistics
  const { data: warehouseStats } = useQuery('warehouse-stats', () =>
    axios.get('/api/inventory/warehouse-stats/').then((res) => res.data)
  );

  // Create mutation
  const createMutation = useMutation(
    (data: WarehouseFormData) => axios.post('/api/inventory/warehouses/', data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('warehouses');
        handleCloseDialog();
        enqueueSnackbar('Warehouse created successfully', { variant: 'success' });
      },
      onError: (error: any) => {
        enqueueSnackbar(error.response?.data?.message || 'Error creating warehouse', {
          variant: 'error',
        });
      },
    }
  );

  // Update mutation
  const updateMutation = useMutation(
    (data: { id: number; warehouse: WarehouseFormData }) =>
      axios.put(`/api/inventory/warehouses/${data.id}/`, data.warehouse),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('warehouses');
        handleCloseDialog();
        enqueueSnackbar('Warehouse updated successfully', { variant: 'success' });
      },
      onError: (error: any) => {
        enqueueSnackbar(error.response?.data?.message || 'Error updating warehouse', {
          variant: 'error',
        });
      },
    }
  );

  // Delete mutation
  const deleteMutation = useMutation(
    (id: number) => axios.delete(`/api/inventory/warehouses/${id}/`),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('warehouses');
        enqueueSnackbar('Warehouse deleted successfully', { variant: 'success' });
      },
      onError: (error: any) => {
        enqueueSnackbar(error.response?.data?.message || 'Error deleting warehouse', {
          variant: 'error',
        });
      },
    }
  );

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleOpenDialog = (warehouse?: Warehouse) => {
    if (warehouse) {
      setSelectedWarehouse(warehouse);
      setFormData({
        name: warehouse.name,
        warehouse_type: warehouse.warehouse_type,
        location: warehouse.location,
        capacity: warehouse.capacity,
        temperature: warehouse.temperature,
        humidity: warehouse.humidity,
        manager_id: warehouse.manager.id,
      });
    } else {
      setSelectedWarehouse(null);
      setFormData({
        name: '',
        warehouse_type: '',
        location: '',
        capacity: 0,
        temperature: 20,
        humidity: 50,
        manager_id: 0,
      });
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedWarehouse(null);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedWarehouse) {
      updateMutation.mutate({ id: selectedWarehouse.id, warehouse: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h5">Warehouses</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Add Warehouse
        </Button>
      </Box>

      {/* Warehouse Statistics */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Stack direction="row" spacing={2} alignItems="center">
                <InventoryIcon color="primary" />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Capacity
                  </Typography>
                  <Typography variant="h6">
                    {warehouseStats?.total_capacity || 0} m³
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Stack direction="row" spacing={2} alignItems="center">
                <InventoryIcon color="success" />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Used Space
                  </Typography>
                  <Typography variant="h6">
                    {warehouseStats?.used_space || 0} m³
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Stack direction="row" spacing={2} alignItems="center">
                <ThermostatIcon color="warning" />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Avg Temperature
                  </Typography>
                  <Typography variant="h6">
                    {warehouseStats?.avg_temperature?.toFixed(1) || 0}°C
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Stack direction="row" spacing={2} alignItems="center">
                <HumidityIcon color="info" />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Avg Humidity
                  </Typography>
                  <Typography variant="h6">
                    {warehouseStats?.avg_humidity?.toFixed(1) || 0}%
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Location</TableCell>
                <TableCell>Manager</TableCell>
                <TableCell>Temperature</TableCell>
                <TableCell>Humidity</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {(warehouses || [])
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((warehouse: Warehouse) => (
                  <TableRow key={warehouse.id}>
                    <TableCell>{warehouse.name}</TableCell>
                    <TableCell>
                      {WAREHOUSE_TYPES.find((t) => t.value === warehouse.warehouse_type)?.label}
                    </TableCell>
                    <TableCell>{warehouse.location}</TableCell>
                    <TableCell>{warehouse.manager.name}</TableCell>
                    <TableCell>{warehouse.temperature}°C</TableCell>
                    <TableCell>{warehouse.humidity}%</TableCell>
                    <TableCell>
                      <IconButton onClick={() => handleOpenDialog(warehouse)}>
                        <EditIcon />
                      </IconButton>
                      <IconButton onClick={() => deleteMutation.mutate(warehouse.id)}>
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={warehouses?.length || 0}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>

      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            {selectedWarehouse ? 'Edit Warehouse' : 'Add Warehouse'}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="Name"
                  value={formData.name}
                  onChange={(e) =>
                    setFormData({ ...formData, name: e.target.value })
                  }
                  required
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  select
                  label="Type"
                  value={formData.warehouse_type}
                  onChange={(e) =>
                    setFormData({ ...formData, warehouse_type: e.target.value })
                  }
                  required
                >
                  {WAREHOUSE_TYPES.map((type) => (
                    <MenuItem key={type.value} value={type.value}>
                      {type.label}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={2}
                  label="Location"
                  value={formData.location}
                  onChange={(e) =>
                    setFormData({ ...formData, location: e.target.value })
                  }
                  required
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="Capacity (m³)"
                  value={formData.capacity}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      capacity: Number(e.target.value),
                    })
                  }
                  required
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  select
                  label="Manager"
                  value={formData.manager_id}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      manager_id: Number(e.target.value),
                    })
                  }
                  required
                >
                  {(users || []).map((user: any) => (
                    <MenuItem key={user.id} value={user.id}>
                      {user.name}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="Temperature (°C)"
                  value={formData.temperature}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      temperature: Number(e.target.value),
                    })
                  }
                  required
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="Humidity (%)"
                  value={formData.humidity}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      humidity: Number(e.target.value),
                    })
                  }
                  required
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Cancel</Button>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={createMutation.isLoading || updateMutation.isLoading}
            >
              {selectedWarehouse ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};

export default Warehouses;
