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
  Typography,
  Chip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  Grid,
  Stack,
  Stepper,
  Step,
  StepLabel,
  Divider,
  Alert,
} from '@mui/material';
import {
  LocalShipping as ShippingIcon,
  Receipt as ReceiptIcon,
  Assignment as OrderIcon,
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import axios from 'axios';
import { format, formatDistanceToNow } from 'date-fns';
import { useNavigate } from 'react-router-dom';

interface OrderItem {
  id: number;
  product: {
    id: number;
    name: string;
    image_url: string;
  };
  quantity: number;
  unit_price: number;
  subtotal: number;
}

interface Order {
  id: number;
  order_number: string;
  status: string;
  payment_status: string;
  shipping_address: string;
  contact_phone: string;
  total_amount: number;
  shipping_fee: number;
  notes: string;
  created_at: string;
  items: OrderItem[];
}

const ORDER_STATUS = {
  PENDING: { label: 'Pending', color: 'default' },
  CONFIRMED: { label: 'Confirmed', color: 'primary' },
  PROCESSING: { label: 'Processing', color: 'info' },
  SHIPPED: { label: 'Shipped', color: 'warning' },
  DELIVERED: { label: 'Delivered', color: 'success' },
  CANCELLED: { label: 'Cancelled', color: 'error' },
};

const PAYMENT_STATUS = {
  PENDING: { label: 'Pending', color: 'warning' },
  PAID: { label: 'Paid', color: 'success' },
  FAILED: { label: 'Failed', color: 'error' },
  REFUNDED: { label: 'Refunded', color: 'info' },
};

const Orders = () => {
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [detailsDialogOpen, setDetailsDialogOpen] = useState(false);

  const navigate = useNavigate();

  // Fetch orders
  const { data: orders, isLoading } = useQuery('orders', () =>
    axios.get('/api/store/orders/').then((res) => res.data)
  );

  const handleOpenDetails = (order: Order) => {
    setSelectedOrder(order);
    setDetailsDialogOpen(true);
  };

  const handleCloseDetails = () => {
    setDetailsDialogOpen(false);
    setSelectedOrder(null);
  };

  const getOrderStatusStep = (status: string) => {
    const steps = ['PENDING', 'CONFIRMED', 'PROCESSING', 'SHIPPED', 'DELIVERED'];
    return steps.indexOf(status);
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!orders?.length) {
    return (
      <Box
        sx={{
          p: 3,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 2,
        }}
      >
        <OrderIcon sx={{ fontSize: 60, color: 'text.secondary' }} />
        <Typography variant="h6" color="text.secondary">
          No orders yet
        </Typography>
        <Button
          variant="contained"
          onClick={() => navigate('/store/products')}
        >
          Start Shopping
        </Button>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 3 }}>
        My Orders
      </Typography>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Order #</TableCell>
              <TableCell>Date</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Payment</TableCell>
              <TableCell align="right">Total</TableCell>
              <TableCell />
            </TableRow>
          </TableHead>
          <TableBody>
            {orders.map((order: Order) => (
              <TableRow key={order.id}>
                <TableCell>{order.order_number}</TableCell>
                <TableCell>
                  {format(new Date(order.created_at), 'MMM d, yyyy')}
                  <Typography variant="caption" display="block" color="text.secondary">
                    {formatDistanceToNow(new Date(order.created_at), {
                      addSuffix: true,
                    })}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Chip
                    label={ORDER_STATUS[order.status as keyof typeof ORDER_STATUS].label}
                    color={ORDER_STATUS[order.status as keyof typeof ORDER_STATUS].color as any}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={PAYMENT_STATUS[order.payment_status as keyof typeof PAYMENT_STATUS].label}
                    color={PAYMENT_STATUS[order.payment_status as keyof typeof PAYMENT_STATUS].color as any}
                    size="small"
                  />
                </TableCell>
                <TableCell align="right">
                  ${(order.total_amount + order.shipping_fee).toFixed(2)}
                </TableCell>
                <TableCell>
                  <Button
                    variant="outlined"
                    size="small"
                    onClick={() => handleOpenDetails(order)}
                  >
                    Details
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Order Details Dialog */}
      <Dialog
        open={detailsDialogOpen}
        onClose={handleCloseDetails}
        maxWidth="md"
        fullWidth
      >
        {selectedOrder && (
          <>
            <DialogTitle>
              Order Details - {selectedOrder.order_number}
            </DialogTitle>
            <DialogContent>
              {selectedOrder.status !== 'CANCELLED' && (
                <Box sx={{ mb: 4 }}>
                  <Stepper
                    activeStep={getOrderStatusStep(selectedOrder.status)}
                    alternativeLabel
                  >
                    <Step>
                      <StepLabel>Order Placed</StepLabel>
                    </Step>
                    <Step>
                      <StepLabel>Confirmed</StepLabel>
                    </Step>
                    <Step>
                      <StepLabel>Processing</StepLabel>
                    </Step>
                    <Step>
                      <StepLabel>Shipped</StepLabel>
                    </Step>
                    <Step>
                      <StepLabel>Delivered</StepLabel>
                    </Step>
                  </Stepper>
                </Box>
              )}

              <Grid container spacing={3}>
                <Grid item xs={12} md={8}>
                  <Typography variant="h6" gutterBottom>
                    Order Items
                  </Typography>
                  <TableContainer component={Paper} variant="outlined">
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Product</TableCell>
                          <TableCell align="center">Quantity</TableCell>
                          <TableCell align="right">Price</TableCell>
                          <TableCell align="right">Subtotal</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {selectedOrder.items.map((item) => (
                          <TableRow key={item.id}>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                                <img
                                  src={item.product.image_url || '/placeholder.png'}
                                  alt={item.product.name}
                                  style={{
                                    width: 40,
                                    height: 40,
                                    objectFit: 'contain',
                                  }}
                                />
                                <Typography variant="body2">
                                  {item.product.name}
                                </Typography>
                              </Box>
                            </TableCell>
                            <TableCell align="center">{item.quantity}</TableCell>
                            <TableCell align="right">
                              ${item.unit_price.toFixed(2)}
                            </TableCell>
                            <TableCell align="right">
                              ${item.subtotal.toFixed(2)}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Grid>

                <Grid item xs={12} md={4}>
                  <Stack spacing={3}>
                    <Paper variant="outlined" sx={{ p: 2 }}>
                      <Typography variant="h6" gutterBottom>
                        Order Summary
                      </Typography>
                      <Stack spacing={2}>
                        <Box
                          sx={{
                            display: 'flex',
                            justifyContent: 'space-between',
                          }}
                        >
                          <Typography color="text.secondary">Subtotal</Typography>
                          <Typography>
                            ${selectedOrder.total_amount.toFixed(2)}
                          </Typography>
                        </Box>
                        <Box
                          sx={{
                            display: 'flex',
                            justifyContent: 'space-between',
                          }}
                        >
                          <Typography color="text.secondary">
                            Shipping Fee
                          </Typography>
                          <Typography>
                            ${selectedOrder.shipping_fee.toFixed(2)}
                          </Typography>
                        </Box>
                        <Divider />
                        <Box
                          sx={{
                            display: 'flex',
                            justifyContent: 'space-between',
                          }}
                        >
                          <Typography variant="subtitle1">Total</Typography>
                          <Typography variant="subtitle1">
                            $
                            {(
                              selectedOrder.total_amount +
                              selectedOrder.shipping_fee
                            ).toFixed(2)}
                          </Typography>
                        </Box>
                      </Stack>
                    </Paper>

                    <Paper variant="outlined" sx={{ p: 2 }}>
                      <Typography variant="h6" gutterBottom>
                        Shipping Information
                      </Typography>
                      <Typography variant="body2" paragraph>
                        {selectedOrder.shipping_address}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Contact: {selectedOrder.contact_phone}
                      </Typography>
                    </Paper>

                    {selectedOrder.notes && (
                      <Paper variant="outlined" sx={{ p: 2 }}>
                        <Typography variant="h6" gutterBottom>
                          Order Notes
                        </Typography>
                        <Typography variant="body2">
                          {selectedOrder.notes}
                        </Typography>
                      </Paper>
                    )}

                    {selectedOrder.status === 'CANCELLED' && (
                      <Alert severity="error">
                        This order has been cancelled
                      </Alert>
                    )}
                  </Stack>
                </Grid>
              </Grid>
            </DialogContent>
          </>
        )}
      </Dialog>
    </Box>
  );
};

export default Orders;
