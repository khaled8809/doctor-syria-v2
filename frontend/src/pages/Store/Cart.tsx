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
  IconButton,
  Button,
  Typography,
  TextField,
  Stack,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Grid,
  Divider,
  Alert,
} from '@mui/material';
import {
  Delete as DeleteIcon,
  Add as AddIcon,
  Remove as RemoveIcon,
  ShoppingCart as CartIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { useSnackbar } from 'notistack';
import { useNavigate } from 'react-router-dom';

interface CartItem {
  id: number;
  product: {
    id: number;
    name: string;
    price: number;
    image_url: string;
    min_order_quantity: number;
    max_order_quantity: number | null;
    requires_prescription: boolean;
  };
  quantity: number;
  prescription?: string;
  subtotal: number;
}

interface Cart {
  id: number;
  items: CartItem[];
  total_amount: number;
}

const Cart = () => {
  const [checkoutDialogOpen, setCheckoutDialogOpen] = useState(false);
  const [shippingAddress, setShippingAddress] = useState('');
  const [contactPhone, setContactPhone] = useState('');
  const [notes, setNotes] = useState('');

  const queryClient = useQueryClient();
  const { enqueueSnackbar } = useSnackbar();
  const navigate = useNavigate();

  // Fetch cart
  const { data: cart, isLoading } = useQuery('cart', () =>
    axios.get('/api/store/cart/').then((res) => res.data)
  );

  // Update cart item mutation
  const updateCartItemMutation = useMutation(
    (data: { id: number; quantity: number }) =>
      axios.patch(`/api/store/cart/items/${data.id}/`, {
        quantity: data.quantity,
      }),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('cart');
      },
      onError: (error: any) => {
        enqueueSnackbar(error.response?.data?.message || 'Error updating cart', {
          variant: 'error',
        });
      },
    }
  );

  // Remove cart item mutation
  const removeCartItemMutation = useMutation(
    (id: number) => axios.delete(`/api/store/cart/items/${id}/`),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('cart');
        enqueueSnackbar('Item removed from cart', { variant: 'success' });
      },
      onError: (error: any) => {
        enqueueSnackbar(error.response?.data?.message || 'Error removing item', {
          variant: 'error',
        });
      },
    }
  );

  // Create order mutation
  const createOrderMutation = useMutation(
    (data: { shipping_address: string; contact_phone: string; notes: string }) =>
      axios.post('/api/store/orders/', data),
    {
      onSuccess: (response) => {
        queryClient.invalidateQueries('cart');
        handleCloseCheckoutDialog();
        enqueueSnackbar('Order placed successfully', { variant: 'success' });
        navigate(`/store/orders/${response.data.id}`);
      },
      onError: (error: any) => {
        enqueueSnackbar(error.response?.data?.message || 'Error creating order', {
          variant: 'error',
        });
      },
    }
  );

  const handleUpdateQuantity = (itemId: number, newQuantity: number) => {
    const item = cart?.items.find((i: CartItem) => i.id === itemId);
    if (!item) return;

    if (
      newQuantity >= item.product.min_order_quantity &&
      (!item.product.max_order_quantity ||
        newQuantity <= item.product.max_order_quantity)
    ) {
      updateCartItemMutation.mutate({ id: itemId, quantity: newQuantity });
    }
  };

  const handleRemoveItem = (itemId: number) => {
    removeCartItemMutation.mutate(itemId);
  };

  const handleCheckout = () => {
    createOrderMutation.mutate({
      shipping_address: shippingAddress,
      contact_phone: contactPhone,
      notes: notes,
    });
  };

  const handleOpenCheckoutDialog = () => {
    setCheckoutDialogOpen(true);
  };

  const handleCloseCheckoutDialog = () => {
    setCheckoutDialogOpen(false);
    setShippingAddress('');
    setContactPhone('');
    setNotes('');
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!cart?.items?.length) {
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
        <CartIcon sx={{ fontSize: 60, color: 'text.secondary' }} />
        <Typography variant="h6" color="text.secondary">
          Your cart is empty
        </Typography>
        <Button
          variant="contained"
          onClick={() => navigate('/store/products')}
        >
          Continue Shopping
        </Button>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 3 }}>
        Shopping Cart
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Product</TableCell>
                  <TableCell align="center">Price</TableCell>
                  <TableCell align="center">Quantity</TableCell>
                  <TableCell align="right">Subtotal</TableCell>
                  <TableCell />
                </TableRow>
              </TableHead>
              <TableBody>
                {cart.items.map((item: CartItem) => (
                  <TableRow key={item.id}>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <img
                          src={item.product.image_url || '/placeholder.png'}
                          alt={item.product.name}
                          style={{
                            width: 50,
                            height: 50,
                            objectFit: 'contain',
                          }}
                        />
                        <Box>
                          <Typography variant="subtitle2">
                            {item.product.name}
                          </Typography>
                          {item.product.requires_prescription && (
                            <Typography
                              variant="caption"
                              color="text.secondary"
                              display="block"
                            >
                              Prescription uploaded
                            </Typography>
                          )}
                        </Box>
                      </Box>
                    </TableCell>
                    <TableCell align="center">
                      ${item.product.price.toFixed(2)}
                    </TableCell>
                    <TableCell align="center">
                      <Stack
                        direction="row"
                        spacing={1}
                        alignItems="center"
                        justifyContent="center"
                      >
                        <IconButton
                          size="small"
                          onClick={() =>
                            handleUpdateQuantity(item.id, item.quantity - 1)
                          }
                          disabled={item.quantity <= item.product.min_order_quantity}
                        >
                          <RemoveIcon />
                        </IconButton>
                        <Typography>{item.quantity}</Typography>
                        <IconButton
                          size="small"
                          onClick={() =>
                            handleUpdateQuantity(item.id, item.quantity + 1)
                          }
                          disabled={
                            item.product.max_order_quantity !== null &&
                            item.quantity >= item.product.max_order_quantity
                          }
                        >
                          <AddIcon />
                        </IconButton>
                      </Stack>
                    </TableCell>
                    <TableCell align="right">
                      ${item.subtotal.toFixed(2)}
                    </TableCell>
                    <TableCell>
                      <IconButton
                        color="error"
                        onClick={() => handleRemoveItem(item.id)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Order Summary
            </Typography>
            <Stack spacing={2}>
              <Box
                sx={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <Typography>Subtotal</Typography>
                <Typography>${cart.total_amount.toFixed(2)}</Typography>
              </Box>
              <Box
                sx={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <Typography>Shipping</Typography>
                <Typography>
                  {cart.total_amount >= 100 ? 'Free' : '$10.00'}
                </Typography>
              </Box>
              <Divider />
              <Box
                sx={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <Typography variant="h6">Total</Typography>
                <Typography variant="h6">
                  $
                  {(
                    cart.total_amount + (cart.total_amount >= 100 ? 0 : 10)
                  ).toFixed(2)}
                </Typography>
              </Box>
              <Button
                fullWidth
                variant="contained"
                size="large"
                onClick={handleOpenCheckoutDialog}
              >
                Proceed to Checkout
              </Button>
            </Stack>
          </Paper>
        </Grid>
      </Grid>

      {/* Checkout Dialog */}
      <Dialog
        open={checkoutDialogOpen}
        onClose={handleCloseCheckoutDialog}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Checkout</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Shipping Address"
                value={shippingAddress}
                onChange={(e) => setShippingAddress(e.target.value)}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Contact Phone"
                value={contactPhone}
                onChange={(e) => setContactPhone(e.target.value)}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={2}
                label="Order Notes"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
              />
            </Grid>
            <Grid item xs={12}>
              <Alert severity="info">
                Free shipping on orders over $100! Current shipping cost:{' '}
                {cart.total_amount >= 100 ? 'Free' : '$10.00'}
              </Alert>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseCheckoutDialog}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleCheckout}
            disabled={!shippingAddress || !contactPhone}
          >
            Place Order
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Cart;
