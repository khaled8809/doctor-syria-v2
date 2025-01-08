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
  Rating,
} from '@mui/material';
import {
  Store,
  LocalShipping,
  Add,
  Edit,
  Delete,
  Inventory,
  ShoppingCart,
  Assessment,
  Business,
  Timeline,
  AttachMoney,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { useSnackbar } from 'notistack';
import { format } from 'date-fns';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface Product {
  id: number;
  name: string;
  manufacturer: string;
  category: string;
  price: number;
  stock: number;
  minimumStock: number;
  description: string;
  image: string;
  rating: number;
  reviews: number;
  sales: number;
}

interface Order {
  id: number;
  customerName: string;
  customerType: 'pharmacy' | 'hospital' | 'clinic';
  items: {
    productId: number;
    productName: string;
    quantity: number;
    price: number;
  }[];
  totalAmount: number;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  paymentStatus: 'pending' | 'paid' | 'refunded';
  createdAt: string;
  shippingAddress: string;
}

interface Manufacturer {
  id: number;
  name: string;
  country: string;
  products: number;
  reliability: number;
  lastDelivery: string;
  contact: {
    email: string;
    phone: string;
    address: string;
  };
}

const CommerceDashboard = () => {
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [newProductDialog, setNewProductDialog] = useState(false);
  const [newOrderDialog, setNewOrderDialog] = useState(false);
  const { enqueueSnackbar } = useSnackbar();
  const queryClient = useQueryClient();

  // Fetch products
  const { data: products, isLoading: loadingProducts } = useQuery<Product[]>(
    'commerce-products',
    () => axios.get('/api/commerce/products/').then((res) => res.data)
  );

  // Fetch orders
  const { data: orders, isLoading: loadingOrders } = useQuery<Order[]>(
    'commerce-orders',
    () => axios.get('/api/commerce/orders/').then((res) => res.data)
  );

  // Fetch manufacturers
  const { data: manufacturers, isLoading: loadingManufacturers } = useQuery<
    Manufacturer[]
  >('commerce-manufacturers', () =>
    axios.get('/api/commerce/manufacturers/').then((res) => res.data)
  );

  // Add new product
  const addProductMutation = useMutation(
    (newProduct: Partial<Product>) =>
      axios.post('/api/commerce/products/', newProduct),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('commerce-products');
        enqueueSnackbar('Product added successfully', {
          variant: 'success',
        });
        setNewProductDialog(false);
      },
    }
  );

  // Add new order
  const addOrderMutation = useMutation(
    (newOrder: Partial<Order>) =>
      axios.post('/api/commerce/orders/', newOrder),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('commerce-orders');
        enqueueSnackbar('Order created successfully', {
          variant: 'success',
        });
        setNewOrderDialog(false);
      },
    }
  );

  const getLowStockProducts = () => {
    return (
      products?.filter((product) => product.stock <= product.minimumStock) || []
    );
  };

  const getTopSellingProducts = () => {
    return (
      [...(products || [])]
        .sort((a, b) => b.sales - a.sales)
        .slice(0, 5) || []
    );
  };

  const renderProducts = () => (
    <Paper sx={{ p: 2 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Products</Typography>
        <Button
          startIcon={<Add />}
          variant="contained"
          onClick={() => setNewProductDialog(true)}
        >
          Add Product
        </Button>
      </Box>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Product</TableCell>
              <TableCell>Manufacturer</TableCell>
              <TableCell align="right">Price</TableCell>
              <TableCell align="right">Stock</TableCell>
              <TableCell>Rating</TableCell>
              <TableCell>Sales</TableCell>
              <TableCell />
            </TableRow>
          </TableHead>
          <TableBody>
            {products?.map((product) => (
              <TableRow key={product.id}>
                <TableCell>
                  <Box display="flex" alignItems="center">
                    <Avatar
                      src={product.image}
                      variant="rounded"
                      sx={{ mr: 2 }}
                    />
                    {product.name}
                  </Box>
                </TableCell>
                <TableCell>{product.manufacturer}</TableCell>
                <TableCell align="right">${product.price}</TableCell>
                <TableCell align="right">
                  <Chip
                    label={product.stock}
                    color={
                      product.stock <= product.minimumStock
                        ? 'error'
                        : 'success'
                    }
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Rating value={product.rating} readOnly size="small" />
                  <Typography variant="caption" display="block">
                    ({product.reviews})
                  </Typography>
                </TableCell>
                <TableCell>{product.sales}</TableCell>
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
              <TableCell>Customer</TableCell>
              <TableCell>Type</TableCell>
              <TableCell align="right">Amount</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Payment</TableCell>
              <TableCell>Date</TableCell>
              <TableCell />
            </TableRow>
          </TableHead>
          <TableBody>
            {orders?.map((order) => (
              <TableRow key={order.id}>
                <TableCell>#{order.id}</TableCell>
                <TableCell>{order.customerName}</TableCell>
                <TableCell>
                  <Chip
                    label={order.customerType}
                    size="small"
                    color="primary"
                  />
                </TableCell>
                <TableCell align="right">${order.totalAmount}</TableCell>
                <TableCell>
                  <Chip
                    label={order.status}
                    color={
                      order.status === 'delivered'
                        ? 'success'
                        : order.status === 'cancelled'
                        ? 'error'
                        : 'warning'
                    }
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={order.paymentStatus}
                    color={
                      order.paymentStatus === 'paid'
                        ? 'success'
                        : order.paymentStatus === 'refunded'
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
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );

  const renderManufacturers = () => (
    <Paper sx={{ p: 2 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Manufacturers</Typography>
        <Button startIcon={<Add />} variant="contained">
          Add Manufacturer
        </Button>
      </Box>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Country</TableCell>
              <TableCell align="right">Products</TableCell>
              <TableCell>Reliability</TableCell>
              <TableCell>Last Delivery</TableCell>
              <TableCell />
            </TableRow>
          </TableHead>
          <TableBody>
            {manufacturers?.map((manufacturer) => (
              <TableRow key={manufacturer.id}>
                <TableCell>{manufacturer.name}</TableCell>
                <TableCell>{manufacturer.country}</TableCell>
                <TableCell align="right">{manufacturer.products}</TableCell>
                <TableCell>
                  <Rating
                    value={manufacturer.reliability}
                    readOnly
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {format(
                    new Date(manufacturer.lastDelivery),
                    'MMM d, yyyy'
                  )}
                </TableCell>
                <TableCell>
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

  const renderSalesChart = () => {
    const salesData = [
      { name: 'Jan', sales: 4000 },
      { name: 'Feb', sales: 3000 },
      { name: 'Mar', sales: 5000 },
      { name: 'Apr', sales: 4500 },
      { name: 'May', sales: 6000 },
      { name: 'Jun', sales: 5500 },
    ];

    return (
      <Paper sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          Sales Overview
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={salesData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="sales"
              stroke="#8884d8"
              activeDot={{ r: 8 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </Paper>
    );
  };

  if (loadingProducts || loadingOrders || loadingManufacturers) {
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
            <Typography variant="h4">E-Commerce Dashboard</Typography>
            <Box>
              <Button
                variant="contained"
                startIcon={<Assessment />}
                color="primary"
                sx={{ mr: 1 }}
              >
                Reports
              </Button>
              <Button
                variant="contained"
                startIcon={<Business />}
                color="primary"
              >
                Manufacturers
              </Button>
            </Box>
          </Box>
        </Grid>

        {/* Stats Cards */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Products
              </Typography>
              <Typography variant="h4">{products?.length || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Orders
              </Typography>
              <Typography variant="h4">{orders?.length || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Revenue
              </Typography>
              <Typography variant="h4">
                $
                {orders
                  ?.reduce((sum, order) => sum + order.totalAmount, 0)
                  .toFixed(2) || '0.00'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Manufacturers
              </Typography>
              <Typography variant="h4">
                {manufacturers?.length || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Sales Chart */}
        <Grid item xs={12}>
          {renderSalesChart()}
        </Grid>

        {/* Products */}
        <Grid item xs={12}>
          {renderProducts()}
        </Grid>

        {/* Orders */}
        <Grid item xs={12}>
          {renderOrders()}
        </Grid>

        {/* Manufacturers */}
        <Grid item xs={12}>
          {renderManufacturers()}
        </Grid>
      </Grid>

      {/* New Product Dialog */}
      <Dialog
        open={newProductDialog}
        onClose={() => setNewProductDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Add New Product</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Product Name"
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Manufacturer"
                select
                SelectProps={{
                  native: true,
                }}
                variant="outlined"
              >
                {manufacturers?.map((manufacturer) => (
                  <option key={manufacturer.id} value={manufacturer.id}>
                    {manufacturer.name}
                  </option>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Category"
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Price"
                type="number"
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Initial Stock"
                type="number"
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Minimum Stock"
                type="number"
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Description"
                multiline
                rows={4}
                variant="outlined"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setNewProductDialog(false)}>Cancel</Button>
          <Button
            variant="contained"
            color="primary"
            disabled={addProductMutation.isLoading}
          >
            Add Product
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default CommerceDashboard;
