import React, { useState } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
} from '@mui/material';
import {
  LocalPharmacy,
  Warning,
  Add,
  Edit,
  Delete,
  Inventory,
  ShoppingCart,
  LocalShipping,
  Notifications,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { useSnackbar } from 'notistack';
import { format } from 'date-fns';

interface Medicine {
  id: number;
  name: string;
  manufacturer: string;
  category: string;
  stock: number;
  price: number;
  expiryDate: string;
  minimumStock: number;
  location: string;
  prescription_required: boolean;
}

interface Order {
  id: number;
  patientName: string;
  doctorName?: string;
  items: {
    medicineId: number;
    medicineName: string;
    quantity: number;
    price: number;
  }[];
  totalAmount: number;
  status: 'pending' | 'processing' | 'completed' | 'cancelled';
  prescriptionVerified: boolean;
  createdAt: string;
}

interface Supplier {
  id: number;
  name: string;
  contact: string;
  email: string;
  lastDelivery: string;
  reliability: number;
}

const PharmacyDashboard = () => {
  const [selectedMedicine, setSelectedMedicine] = useState<Medicine | null>(null);
  const [newOrderDialog, setNewOrderDialog] = useState(false);
  const [restockDialog, setRestockDialog] = useState(false);
  const { enqueueSnackbar } = useSnackbar();
  const queryClient = useQueryClient();

  // Fetch inventory
  const { data: inventory, isLoading: loadingInventory } = useQuery<Medicine[]>(
    'pharmacy-inventory',
    () => axios.get('/api/pharmacy/inventory/').then((res) => res.data)
  );

  // Fetch orders
  const { data: orders, isLoading: loadingOrders } = useQuery<Order[]>(
    'pharmacy-orders',
    () => axios.get('/api/pharmacy/orders/').then((res) => res.data)
  );

  // Fetch suppliers
  const { data: suppliers, isLoading: loadingSuppliers } = useQuery<Supplier[]>(
    'pharmacy-suppliers',
    () => axios.get('/api/pharmacy/suppliers/').then((res) => res.data)
  );

  // Add new order
  const addOrderMutation = useMutation(
    (newOrder: Partial<Order>) =>
      axios.post('/api/pharmacy/orders/', newOrder),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('pharmacy-orders');
        enqueueSnackbar('Order created successfully', {
          variant: 'success',
        });
        setNewOrderDialog(false);
      },
    }
  );

  // Restock inventory
  const restockMutation = useMutation(
    (data: { medicineId: number; quantity: number }) =>
      axios.post('/api/pharmacy/inventory/restock/', data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('pharmacy-inventory');
        enqueueSnackbar('Inventory restocked successfully', {
          variant: 'success',
        });
        setRestockDialog(false);
      },
    }
  );

  const getLowStockItems = () => {
    return (
      inventory?.filter((item) => item.stock <= item.minimumStock) || []
    );
  };

  const getExpiringItems = () => {
    const thirtyDaysFromNow = new Date();
    thirtyDaysFromNow.setDate(thirtyDaysFromNow.getDate() + 30);
    
    return (
      inventory?.filter(
        (item) => new Date(item.expiryDate) <= thirtyDaysFromNow
      ) || []
    );
  };

  const renderInventory = () => (
    <Paper sx={{ p: 2 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Inventory</Typography>
        <Button startIcon={<Add />} variant="contained">
          Add Medicine
        </Button>
      </Box>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Medicine</TableCell>
              <TableCell>Category</TableCell>
              <TableCell align="right">Stock</TableCell>
              <TableCell align="right">Price</TableCell>
              <TableCell>Expiry</TableCell>
              <TableCell>Status</TableCell>
              <TableCell />
            </TableRow>
          </TableHead>
          <TableBody>
            {inventory?.map((medicine) => (
              <TableRow key={medicine.id}>
                <TableCell>{medicine.name}</TableCell>
                <TableCell>{medicine.category}</TableCell>
                <TableCell align="right">{medicine.stock}</TableCell>
                <TableCell align="right">${medicine.price}</TableCell>
                <TableCell>
                  {format(new Date(medicine.expiryDate), 'MMM d, yyyy')}
                </TableCell>
                <TableCell>
                  {medicine.stock <= medicine.minimumStock ? (
                    <Chip
                      label="Low Stock"
                      color="error"
                      size="small"
                    />
                  ) : (
                    <Chip
                      label="In Stock"
                      color="success"
                      size="small"
                    />
                  )}
                </TableCell>
                <TableCell>
                  <IconButton
                    size="small"
                    onClick={() => {
                      setSelectedMedicine(medicine);
                      setRestockDialog(true);
                    }}
                  >
                    <Add />
                  </IconButton>
                  <IconButton size="small">
                    <Edit />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );

  const renderOrders = () => (
    <Paper sx={{ p: 2 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Recent Orders</Typography>
        <Button
          startIcon={<Add />}
          variant="contained"
          onClick={() => setNewOrderDialog(true)}
        >
          New Order
        </Button>
      </Box>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Order ID</TableCell>
              <TableCell>Patient</TableCell>
              <TableCell>Items</TableCell>
              <TableCell align="right">Total</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Created</TableCell>
              <TableCell />
            </TableRow>
          </TableHead>
          <TableBody>
            {orders?.map((order) => (
              <TableRow key={order.id}>
                <TableCell>#{order.id}</TableCell>
                <TableCell>{order.patientName}</TableCell>
                <TableCell>{order.items.length} items</TableCell>
                <TableCell align="right">${order.totalAmount}</TableCell>
                <TableCell>
                  <Chip
                    label={order.status}
                    color={
                      order.status === 'completed'
                        ? 'success'
                        : order.status === 'cancelled'
                        ? 'error'
                        : 'warning'
                    }
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {format(new Date(order.createdAt), 'MMM d, HH:mm')}
                </TableCell>
                <TableCell>
                  <IconButton size="small">
                    <Edit />
                  </IconButton>
                  <IconButton size="small">
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );

  const renderAlerts = () => (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Alerts
      </Typography>
      <Grid container spacing={2}>
        {/* Low Stock Alerts */}
        <Grid item xs={12}>
          <Alert
            severity="warning"
            icon={<Inventory />}
            action={
              <Button color="inherit" size="small">
                View All
              </Button>
            }
          >
            {getLowStockItems().length} items are running low on stock
          </Alert>
        </Grid>

        {/* Expiring Items */}
        <Grid item xs={12}>
          <Alert
            severity="error"
            icon={<Warning />}
            action={
              <Button color="inherit" size="small">
                View All
              </Button>
            }
          >
            {getExpiringItems().length} items are expiring within 30 days
          </Alert>
        </Grid>
      </Grid>
    </Paper>
  );

  if (loadingInventory || loadingOrders || loadingSuppliers) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="400px"
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Grid container spacing={3}>
        {/* Header */}
        <Grid item xs={12}>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h4">Pharmacy Dashboard</Typography>
            <Box>
              <IconButton color="primary" sx={{ mr: 1 }}>
                <Notifications />
              </IconButton>
              <Button
                variant="contained"
                startIcon={<LocalShipping />}
                color="primary"
              >
                Supplier Orders
              </Button>
            </Box>
          </Box>
        </Grid>

        {/* Stats Cards */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Inventory
              </Typography>
              <Typography variant="h4">
                {inventory?.reduce((sum, item) => sum + item.stock, 0) || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Today's Orders
              </Typography>
              <Typography variant="h4">
                {orders?.filter((order) =>
                  format(new Date(order.createdAt), 'yyyy-MM-dd') ===
                  format(new Date(), 'yyyy-MM-dd')
                ).length || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Low Stock Items
              </Typography>
              <Typography variant="h4" color="error">
                {getLowStockItems().length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Today's Revenue
              </Typography>
              <Typography variant="h4">
                $
                {orders
                  ?.filter(
                    (order) =>
                      format(new Date(order.createdAt), 'yyyy-MM-dd') ===
                        format(new Date(), 'yyyy-MM-dd') &&
                      order.status === 'completed'
                  )
                  .reduce((sum, order) => sum + order.totalAmount, 0)
                  .toFixed(2) || '0.00'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Alerts */}
        <Grid item xs={12}>
          {renderAlerts()}
        </Grid>

        {/* Inventory */}
        <Grid item xs={12}>
          {renderInventory()}
        </Grid>

        {/* Orders */}
        <Grid item xs={12}>
          {renderOrders()}
        </Grid>
      </Grid>

      {/* Restock Dialog */}
      <Dialog
        open={restockDialog}
        onClose={() => setRestockDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Restock Inventory</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Medicine"
                value={selectedMedicine?.name}
                disabled
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Current Stock"
                value={selectedMedicine?.stock}
                disabled
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Quantity to Add"
                type="number"
                variant="outlined"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setRestockDialog(false)}>Cancel</Button>
          <Button
            variant="contained"
            color="primary"
            disabled={restockMutation.isLoading}
          >
            Restock
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PharmacyDashboard;
