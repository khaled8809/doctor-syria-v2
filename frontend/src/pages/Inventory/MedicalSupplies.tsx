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
  Chip,
  Tooltip,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { useSnackbar } from 'notistack';

interface MedicalSupply {
  id: number;
  name: string;
  code: string;
  supply_type: string;
  manufacturer: {
    id: number;
    name: string;
  };
  description: string;
  unit: string;
  minimum_quantity: number;
  storage_condition: string;
  expiry_alert_days: number;
  is_active: boolean;
}

interface SupplyFormData {
  name: string;
  code: string;
  supply_type: string;
  manufacturer_id: number;
  description: string;
  unit: string;
  minimum_quantity: number;
  storage_condition: string;
  expiry_alert_days: number;
}

const SUPPLY_TYPES = [
  { value: 'MEDICATION', label: 'Medication' },
  { value: 'EQUIPMENT', label: 'Medical Equipment' },
  { value: 'DISPOSABLE', label: 'Disposable Supply' },
  { value: 'INSTRUMENT', label: 'Medical Instrument' },
];

const STORAGE_CONDITIONS = [
  { value: 'NORMAL', label: 'Normal' },
  { value: 'REFRIGERATED', label: 'Refrigerated' },
  { value: 'FROZEN', label: 'Frozen' },
  { value: 'CONTROLLED', label: 'Controlled Substance' },
];

const MedicalSupplies = () => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedSupply, setSelectedSupply] = useState<MedicalSupply | null>(null);
  const [formData, setFormData] = useState<SupplyFormData>({
    name: '',
    code: '',
    supply_type: '',
    manufacturer_id: 0,
    description: '',
    unit: '',
    minimum_quantity: 0,
    storage_condition: '',
    expiry_alert_days: 90,
  });

  const queryClient = useQueryClient();
  const { enqueueSnackbar } = useSnackbar();

  // Fetch medical supplies
  const { data: supplies, isLoading } = useQuery('medical-supplies', () =>
    axios.get('/api/inventory/medical-supplies/').then((res) => res.data)
  );

  // Fetch manufacturers
  const { data: manufacturers } = useQuery('manufacturers', () =>
    axios.get('/api/inventory/manufacturers/').then((res) => res.data)
  );

  // Fetch inventory levels
  const { data: inventoryLevels } = useQuery('inventory-levels', () =>
    axios.get('/api/inventory/levels/').then((res) => res.data)
  );

  // Create mutation
  const createMutation = useMutation(
    (data: SupplyFormData) =>
      axios.post('/api/inventory/medical-supplies/', data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('medical-supplies');
        handleCloseDialog();
        enqueueSnackbar('Medical supply created successfully', {
          variant: 'success',
        });
      },
      onError: (error: any) => {
        enqueueSnackbar(error.response?.data?.message || 'Error creating medical supply', {
          variant: 'error',
        });
      },
    }
  );

  // Update mutation
  const updateMutation = useMutation(
    (data: { id: number; supply: SupplyFormData }) =>
      axios.put(`/api/inventory/medical-supplies/${data.id}/`, data.supply),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('medical-supplies');
        handleCloseDialog();
        enqueueSnackbar('Medical supply updated successfully', {
          variant: 'success',
        });
      },
      onError: (error: any) => {
        enqueueSnackbar(error.response?.data?.message || 'Error updating medical supply', {
          variant: 'error',
        });
      },
    }
  );

  // Delete mutation
  const deleteMutation = useMutation(
    (id: number) => axios.delete(`/api/inventory/medical-supplies/${id}/`),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('medical-supplies');
        enqueueSnackbar('Medical supply deleted successfully', {
          variant: 'success',
        });
      },
      onError: (error: any) => {
        enqueueSnackbar(error.response?.data?.message || 'Error deleting medical supply', {
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

  const handleOpenDialog = (supply?: MedicalSupply) => {
    if (supply) {
      setSelectedSupply(supply);
      setFormData({
        name: supply.name,
        code: supply.code,
        supply_type: supply.supply_type,
        manufacturer_id: supply.manufacturer.id,
        description: supply.description,
        unit: supply.unit,
        minimum_quantity: supply.minimum_quantity,
        storage_condition: supply.storage_condition,
        expiry_alert_days: supply.expiry_alert_days,
      });
    } else {
      setSelectedSupply(null);
      setFormData({
        name: '',
        code: '',
        supply_type: '',
        manufacturer_id: 0,
        description: '',
        unit: '',
        minimum_quantity: 0,
        storage_condition: '',
        expiry_alert_days: 90,
      });
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedSupply(null);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedSupply) {
      updateMutation.mutate({ id: selectedSupply.id, supply: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const getInventoryStatus = (supplyId: number) => {
    const level = inventoryLevels?.[supplyId];
    if (!level) return null;

    if (level.quantity <= level.minimum_quantity) {
      return (
        <Tooltip title="Low Stock">
          <Chip
            icon={<WarningIcon />}
            label={`Low: ${level.quantity} ${level.unit}`}
            color="warning"
            size="small"
          />
        </Tooltip>
      );
    }
    return (
      <Tooltip title="Stock OK">
        <Chip
          icon={<CheckCircleIcon />}
          label={`${level.quantity} ${level.unit}`}
          color="success"
          size="small"
        />
      </Tooltip>
    );
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h5">Medical Supplies</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Add Supply
        </Button>
      </Box>

      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Code</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Manufacturer</TableCell>
                <TableCell>Storage</TableCell>
                <TableCell>Current Stock</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {(supplies || [])
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((supply: MedicalSupply) => (
                  <TableRow key={supply.id}>
                    <TableCell>{supply.code}</TableCell>
                    <TableCell>{supply.name}</TableCell>
                    <TableCell>
                      {SUPPLY_TYPES.find((t) => t.value === supply.supply_type)?.label}
                    </TableCell>
                    <TableCell>{supply.manufacturer.name}</TableCell>
                    <TableCell>
                      {STORAGE_CONDITIONS.find((s) => s.value === supply.storage_condition)?.label}
                    </TableCell>
                    <TableCell>{getInventoryStatus(supply.id)}</TableCell>
                    <TableCell>
                      <IconButton onClick={() => handleOpenDialog(supply)}>
                        <EditIcon />
                      </IconButton>
                      <IconButton onClick={() => deleteMutation.mutate(supply.id)}>
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
          count={supplies?.length || 0}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>

      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            {selectedSupply ? 'Edit Medical Supply' : 'Add Medical Supply'}
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
                  label="Code"
                  value={formData.code}
                  onChange={(e) =>
                    setFormData({ ...formData, code: e.target.value })
                  }
                  required
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  select
                  label="Type"
                  value={formData.supply_type}
                  onChange={(e) =>
                    setFormData({ ...formData, supply_type: e.target.value })
                  }
                  required
                >
                  {SUPPLY_TYPES.map((type) => (
                    <MenuItem key={type.value} value={type.value}>
                      {type.label}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  select
                  label="Manufacturer"
                  value={formData.manufacturer_id}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      manufacturer_id: Number(e.target.value),
                    })
                  }
                  required
                >
                  {(manufacturers || []).map((manufacturer: any) => (
                    <MenuItem key={manufacturer.id} value={manufacturer.id}>
                      {manufacturer.name}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  label="Description"
                  value={formData.description}
                  onChange={(e) =>
                    setFormData({ ...formData, description: e.target.value })
                  }
                  required
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="Unit"
                  value={formData.unit}
                  onChange={(e) =>
                    setFormData({ ...formData, unit: e.target.value })
                  }
                  required
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="Minimum Quantity"
                  value={formData.minimum_quantity}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      minimum_quantity: Number(e.target.value),
                    })
                  }
                  required
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  select
                  label="Storage Condition"
                  value={formData.storage_condition}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      storage_condition: e.target.value,
                    })
                  }
                  required
                >
                  {STORAGE_CONDITIONS.map((condition) => (
                    <MenuItem key={condition.value} value={condition.value}>
                      {condition.label}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="Expiry Alert Days"
                  value={formData.expiry_alert_days}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      expiry_alert_days: Number(e.target.value),
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
              {selectedSupply ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};

export default MedicalSupplies;
