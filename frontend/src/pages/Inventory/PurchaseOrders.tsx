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
  Stepper,
  Step,
  StepLabel,
  Chip,
  Stack,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  CheckCircle as ApproveIcon,
  Cancel as RejectIcon,
  LocalShipping as ReceiveIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { useSnackbar } from 'notistack';
import { format } from 'date-fns';

interface PurchaseOrder {
  id: number;
  order_number: string;
  supplier: {
    id: number;
    name: string;
  };
  status: string;
  total_amount: number;
  expected_delivery_date: string;
  created_by: {
    id: number;
    name: string;
  };
  created_at: string;
  notes: string;
  items: PurchaseOrderItem[];
}

interface PurchaseOrderItem {
  id: number;
  supply: {
    id: number;
    name: string;
    code: string;
    unit: string;
  };
  quantity: number;
  unit_price: number;
  total_price: number;
}

const ORDER_STATUS = {
  DRAFT: 'Draft',
  PENDING_APPROVAL: 'Pending Approval',
  APPROVED: 'Approved',
  REJECTED: 'Rejected',
  ORDERED: 'Ordered',
  PARTIALLY_RECEIVED: 'Partially Received',
  RECEIVED: 'Received',
  CANCELLED: 'Cancelled',
};

const ORDER_STATUS_COLORS: { [key: string]: 'default' | 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning' } = {
  DRAFT: 'default',
  PENDING_APPROVAL: 'warning',
  APPROVED: 'success',
  REJECTED: 'error',
  ORDERED: 'primary',
  PARTIALLY_RECEIVED: 'info',
  RECEIVED: 'success',
  CANCELLED: 'error',
};

const PurchaseOrders = () => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState<PurchaseOrder | null>(null);
  const [formData, setFormData] = useState({
    supplier_id: '',
    expected_delivery_date: '',
    notes: '',
    items: [{ supply_id: '', quantity: 0, unit_price: 0 }],
  });

  const queryClient = useQueryClient();
  const { enqueueSnackbar } = useSnackbar();

  // Fetch purchase orders
  const { data: purchaseOrders, isLoading } = useQuery('purchase-orders', () =>
    axios.get('/api/inventory/purchase-orders/').then((res) => res.data)
  );

  // Fetch suppliers
  const { data: suppliers } = useQuery('suppliers', () =>
    axios.get('/api/inventory/suppliers/').then((res) => res.data)
  );

  // Fetch supplies
  const { data: supplies } = useQuery('supplies', () =>
    axios.get('/api/inventory/supplies/').then((res) => res.data)
  );

  // Create mutation
  const createMutation = useMutation(
    (data: any) => axios.post('/api/inventory/purchase-orders/', data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('purchase-orders');
        handleCloseDialog();
        enqueueSnackbar('Purchase order created successfully', {
          variant: 'success',
        });
      },
      onError: (error: any) => {
        enqueueSnackbar(error.response?.data?.message || 'Error creating purchase order', {
          variant: 'error',
        });
      },
    }
  );

  // Update status mutation
  const updateStatusMutation = useMutation(
    (data: { id: number; status: string }) =>
      axios.patch(`/api/inventory/purchase-orders/${data.id}/status/`, {
        status: data.status,
      }),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('purchase-orders');
        enqueueSnackbar('Purchase order status updated successfully', {
          variant: 'success',
        });
      },
      onError: (error: any) => {
        enqueueSnackbar(error.response?.data?.message || 'Error updating status', {
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

  const handleOpenDialog = (order?: PurchaseOrder) => {
    if (order) {
      setSelectedOrder(order);
      setFormData({
        supplier_id: order.supplier.id.toString(),
        expected_delivery_date: order.expected_delivery_date,
        notes: order.notes,
        items: order.items.map((item) => ({
          supply_id: item.supply.id.toString(),
          quantity: item.quantity,
          unit_price: item.unit_price,
        })),
      });
    } else {
      setSelectedOrder(null);
      setFormData({
        supplier_id: '',
        expected_delivery_date: '',
        notes: '',
        items: [{ supply_id: '', quantity: 0, unit_price: 0 }],
      });
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedOrder(null);
  };

  const handleAddItem = () => {
    setFormData({
      ...formData,
      items: [
        ...formData.items,
        { supply_id: '', quantity: 0, unit_price: 0 },
      ],
    });
  };

  const handleRemoveItem = (index: number) => {
    setFormData({
      ...formData,
      items: formData.items.filter((_, i) => i !== index),
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate(formData);
  };

  const getOrderStatusStep = (status: string) => {
    const steps = [
      'DRAFT',
      'PENDING_APPROVAL',
      'APPROVED',
      'ORDERED',
      'PARTIALLY_RECEIVED',
      'RECEIVED',
    ];
    return steps.indexOf(status);
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h5">Purchase Orders</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          New Order
        </Button>
      </Box>

      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Order #</TableCell>
                <TableCell>Supplier</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Total Amount</TableCell>
                <TableCell>Expected Delivery</TableCell>
                <TableCell>Created By</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {(purchaseOrders || [])
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((order: PurchaseOrder) => (
                  <TableRow key={order.id}>
                    <TableCell>{order.order_number}</TableCell>
                    <TableCell>{order.supplier.name}</TableCell>
                    <TableCell>
                      <Chip
                        label={ORDER_STATUS[order.status as keyof typeof ORDER_STATUS]}
                        color={ORDER_STATUS_COLORS[order.status]}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>${order.total_amount.toFixed(2)}</TableCell>
                    <TableCell>
                      {format(new Date(order.expected_delivery_date), 'dd/MM/yyyy')}
                    </TableCell>
                    <TableCell>{order.created_by.name}</TableCell>
                    <TableCell>
                      <Stack direction="row" spacing={1}>
                        {order.status === 'PENDING_APPROVAL' && (
                          <>
                            <IconButton
                              onClick={() =>
                                updateStatusMutation.mutate({
                                  id: order.id,
                                  status: 'APPROVED',
                                })
                              }
                            >
                              <ApproveIcon color="success" />
                            </IconButton>
                            <IconButton
                              onClick={() =>
                                updateStatusMutation.mutate({
                                  id: order.id,
                                  status: 'REJECTED',
                                })
                              }
                            >
                              <RejectIcon color="error" />
                            </IconButton>
                          </>
                        )}
                        {order.status === 'ORDERED' && (
                          <IconButton
                            onClick={() =>
                              updateStatusMutation.mutate({
                                id: order.id,
                                status: 'RECEIVED',
                              })
                            }
                          >
                            <ReceiveIcon color="primary" />
                          </IconButton>
                        )}
                        {order.status === 'DRAFT' && (
                          <>
                            <IconButton onClick={() => handleOpenDialog(order)}>
                              <EditIcon />
                            </IconButton>
                            <IconButton
                              onClick={() =>
                                updateStatusMutation.mutate({
                                  id: order.id,
                                  status: 'CANCELLED',
                                })
                              }
                            >
                              <DeleteIcon />
                            </IconButton>
                          </>
                        )}
                      </Stack>
                    </TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={purchaseOrders?.length || 0}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>

      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            {selectedOrder ? 'Edit Purchase Order' : 'New Purchase Order'}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  select
                  label="Supplier"
                  value={formData.supplier_id}
                  onChange={(e) =>
                    setFormData({ ...formData, supplier_id: e.target.value })
                  }
                  required
                >
                  {(suppliers || []).map((supplier: any) => (
                    <MenuItem key={supplier.id} value={supplier.id}>
                      {supplier.name}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  type="date"
                  label="Expected Delivery Date"
                  value={formData.expected_delivery_date}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      expected_delivery_date: e.target.value,
                    })
                  }
                  InputLabelProps={{ shrink: true }}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle1" sx={{ mb: 2 }}>
                  Order Items
                </Typography>
                {formData.items.map((item, index) => (
                  <Box key={index} sx={{ mb: 2 }}>
                    <Grid container spacing={2}>
                      <Grid item xs={5}>
                        <TextField
                          fullWidth
                          select
                          label="Supply"
                          value={item.supply_id}
                          onChange={(e) => {
                            const newItems = [...formData.items];
                            newItems[index].supply_id = e.target.value;
                            setFormData({ ...formData, items: newItems });
                          }}
                          required
                        >
                          {(supplies || []).map((supply: any) => (
                            <MenuItem key={supply.id} value={supply.id}>
                              {supply.name}
                            </MenuItem>
                          ))}
                        </TextField>
                      </Grid>
                      <Grid item xs={3}>
                        <TextField
                          fullWidth
                          type="number"
                          label="Quantity"
                          value={item.quantity}
                          onChange={(e) => {
                            const newItems = [...formData.items];
                            newItems[index].quantity = Number(e.target.value);
                            setFormData({ ...formData, items: newItems });
                          }}
                          required
                        />
                      </Grid>
                      <Grid item xs={3}>
                        <TextField
                          fullWidth
                          type="number"
                          label="Unit Price"
                          value={item.unit_price}
                          onChange={(e) => {
                            const newItems = [...formData.items];
                            newItems[index].unit_price = Number(e.target.value);
                            setFormData({ ...formData, items: newItems });
                          }}
                          required
                        />
                      </Grid>
                      <Grid item xs={1}>
                        <IconButton
                          onClick={() => handleRemoveItem(index)}
                          disabled={formData.items.length === 1}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Grid>
                    </Grid>
                  </Box>
                ))}
                <Button
                  startIcon={<AddIcon />}
                  onClick={handleAddItem}
                  sx={{ mt: 1 }}
                >
                  Add Item
                </Button>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  label="Notes"
                  value={formData.notes}
                  onChange={(e) =>
                    setFormData({ ...formData, notes: e.target.value })
                  }
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
              disabled={createMutation.isLoading}
            >
              {selectedOrder ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};

export default PurchaseOrders;
