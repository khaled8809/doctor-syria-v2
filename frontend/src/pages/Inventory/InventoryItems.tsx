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
  Chip,
  Tabs,
  Tab,
  Alert,
  AlertTitle,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  SwapHoriz as TransferIcon,
  Warning as WarningIcon,
  LocalShipping as ReceiveIcon,
  ShoppingCart as DispenseIcon,
  Timeline as TimelineIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { useSnackbar } from 'notistack';
import { format, formatDistanceToNow } from 'date-fns';

interface InventoryItem {
  id: number;
  supply: {
    id: number;
    name: string;
    code: string;
    unit: string;
  };
  warehouse: {
    id: number;
    name: string;
  };
  batch_number: string;
  quantity: number;
  unit_price: number;
  manufacturing_date: string;
  expiry_date: string;
  location_in_warehouse: string;
  is_quarantined: boolean;
  quarantine_reason: string;
}

interface Transaction {
  id: number;
  transaction_type: string;
  quantity: number;
  reference_number: string;
  performed_by: {
    id: number;
    name: string;
  };
  created_at: string;
  source_location?: {
    id: number;
    name: string;
  };
  destination_location?: {
    id: number;
    name: string;
  };
  notes: string;
}

const TRANSACTION_TYPES = {
  RECEIVE: 'Receive',
  DISPENSE: 'Dispense',
  TRANSFER: 'Transfer',
  RETURN: 'Return',
  DISPOSE: 'Dispose',
  ADJUST: 'Adjustment',
};

const InventoryItems = () => {
  const [tabValue, setTabValue] = useState(0);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [transactionDialogOpen, setTransactionDialogOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState<InventoryItem | null>(null);
  const [transactionType, setTransactionType] = useState('');
  const [transactionData, setTransactionData] = useState({
    quantity: 0,
    reference_number: '',
    destination_warehouse_id: '',
    notes: '',
  });

  const queryClient = useQueryClient();
  const { enqueueSnackbar } = useSnackbar();

  // Fetch inventory items
  const { data: inventoryItems, isLoading } = useQuery('inventory-items', () =>
    axios.get('/api/inventory/items/').then((res) => res.data)
  );

  // Fetch transactions
  const { data: transactions } = useQuery('inventory-transactions', () =>
    axios.get('/api/inventory/transactions/').then((res) => res.data)
  );

  // Fetch warehouses
  const { data: warehouses } = useQuery('warehouses', () =>
    axios.get('/api/inventory/warehouses/').then((res) => res.data)
  );

  // Fetch supplies
  const { data: supplies } = useQuery('supplies', () =>
    axios.get('/api/inventory/supplies/').then((res) => res.data)
  );

  // Transaction mutation
  const transactionMutation = useMutation(
    (data: any) => axios.post('/api/inventory/transactions/', data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('inventory-items');
        queryClient.invalidateQueries('inventory-transactions');
        handleCloseTransactionDialog();
        enqueueSnackbar('Transaction completed successfully', {
          variant: 'success',
        });
      },
      onError: (error: any) => {
        enqueueSnackbar(error.response?.data?.message || 'Error processing transaction', {
          variant: 'error',
        });
      },
    }
  );

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleChangePage = (event: unknown, newValue: number) => {
    setPage(newValue);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleOpenTransactionDialog = (item: InventoryItem, type: string) => {
    setSelectedItem(item);
    setTransactionType(type);
    setTransactionDialogOpen(true);
  };

  const handleCloseTransactionDialog = () => {
    setTransactionDialogOpen(false);
    setSelectedItem(null);
    setTransactionType('');
    setTransactionData({
      quantity: 0,
      reference_number: '',
      destination_warehouse_id: '',
      notes: '',
    });
  };

  const handleTransactionSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedItem) return;

    const data = {
      inventory_item_id: selectedItem.id,
      transaction_type: transactionType,
      ...transactionData,
    };

    transactionMutation.mutate(data);
  };

  const getStatusChip = (item: InventoryItem) => {
    if (item.is_quarantined) {
      return (
        <Chip
          label="Quarantined"
          color="error"
          size="small"
          icon={<WarningIcon />}
        />
      );
    }

    const expiryDate = new Date(item.expiry_date);
    const today = new Date();
    const daysToExpiry = Math.ceil(
      (expiryDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24)
    );

    if (daysToExpiry <= 0) {
      return (
        <Chip label="Expired" color="error" size="small" icon={<WarningIcon />} />
      );
    }

    if (daysToExpiry <= 90) {
      return (
        <Chip
          label={`Expires in ${daysToExpiry} days`}
          color="warning"
          size="small"
          icon={<WarningIcon />}
        />
      );
    }

    return <Chip label="OK" color="success" size="small" />;
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 3 }}>
        Inventory Management
      </Typography>

      {/* Alerts for attention items */}
      <Stack spacing={2} sx={{ mb: 3 }}>
        {inventoryItems?.some((item: InventoryItem) => item.is_quarantined) && (
          <Alert severity="error">
            <AlertTitle>Quarantined Items</AlertTitle>
            There are items in quarantine that need attention
          </Alert>
        )}
        {inventoryItems?.some(
          (item: InventoryItem) =>
            new Date(item.expiry_date) <= new Date()
        ) && (
          <Alert severity="warning">
            <AlertTitle>Expired Items</AlertTitle>
            There are expired items in inventory
          </Alert>
        )}
      </Stack>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="Inventory Items" />
          <Tab label="Transactions" />
        </Tabs>
      </Box>

      {/* Inventory Items Tab */}
      <TabPanel value={tabValue} index={0}>
        <Paper>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Supply</TableCell>
                  <TableCell>Warehouse</TableCell>
                  <TableCell>Batch</TableCell>
                  <TableCell>Quantity</TableCell>
                  <TableCell>Location</TableCell>
                  <TableCell>Expiry Date</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {(inventoryItems || [])
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((item: InventoryItem) => (
                    <TableRow key={item.id}>
                      <TableCell>
                        {item.supply.name}
                        <Typography variant="caption" display="block" color="textSecondary">
                          {item.supply.code}
                        </Typography>
                      </TableCell>
                      <TableCell>{item.warehouse.name}</TableCell>
                      <TableCell>{item.batch_number}</TableCell>
                      <TableCell>
                        {item.quantity} {item.supply.unit}
                      </TableCell>
                      <TableCell>{item.location_in_warehouse}</TableCell>
                      <TableCell>
                        {format(new Date(item.expiry_date), 'dd/MM/yyyy')}
                      </TableCell>
                      <TableCell>{getStatusChip(item)}</TableCell>
                      <TableCell>
                        <IconButton
                          onClick={() => handleOpenTransactionDialog(item, 'RECEIVE')}
                        >
                          <ReceiveIcon />
                        </IconButton>
                        <IconButton
                          onClick={() => handleOpenTransactionDialog(item, 'DISPENSE')}
                        >
                          <DispenseIcon />
                        </IconButton>
                        <IconButton
                          onClick={() => handleOpenTransactionDialog(item, 'TRANSFER')}
                        >
                          <TransferIcon />
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
            count={inventoryItems?.length || 0}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Paper>
      </TabPanel>

      {/* Transactions Tab */}
      <TabPanel value={tabValue} index={1}>
        <Paper>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Date</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Reference</TableCell>
                  <TableCell>Item</TableCell>
                  <TableCell>Quantity</TableCell>
                  <TableCell>From</TableCell>
                  <TableCell>To</TableCell>
                  <TableCell>Performed By</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {(transactions || [])
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((transaction: Transaction) => (
                    <TableRow key={transaction.id}>
                      <TableCell>
                        {formatDistanceToNow(new Date(transaction.created_at), {
                          addSuffix: true,
                        })}
                      </TableCell>
                      <TableCell>
                        {TRANSACTION_TYPES[transaction.transaction_type as keyof typeof TRANSACTION_TYPES]}
                      </TableCell>
                      <TableCell>{transaction.reference_number}</TableCell>
                      <TableCell>
                        {inventoryItems?.find(
                          (item: InventoryItem) =>
                            item.id === transaction.id
                        )?.supply.name}
                      </TableCell>
                      <TableCell>{transaction.quantity}</TableCell>
                      <TableCell>
                        {transaction.source_location?.name || '-'}
                      </TableCell>
                      <TableCell>
                        {transaction.destination_location?.name || '-'}
                      </TableCell>
                      <TableCell>{transaction.performed_by.name}</TableCell>
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={transactions?.length || 0}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Paper>
      </TabPanel>

      {/* Transaction Dialog */}
      <Dialog
        open={transactionDialogOpen}
        onClose={handleCloseTransactionDialog}
        maxWidth="sm"
        fullWidth
      >
        <form onSubmit={handleTransactionSubmit}>
          <DialogTitle>
            {TRANSACTION_TYPES[transactionType as keyof typeof TRANSACTION_TYPES]}{' '}
            Item
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <Typography variant="subtitle1">
                  {selectedItem?.supply.name} - {selectedItem?.batch_number}
                </Typography>
                <Typography color="textSecondary">
                  Current Quantity: {selectedItem?.quantity}{' '}
                  {selectedItem?.supply.unit}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  type="number"
                  label="Quantity"
                  value={transactionData.quantity}
                  onChange={(e) =>
                    setTransactionData({
                      ...transactionData,
                      quantity: Number(e.target.value),
                    })
                  }
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Reference Number"
                  value={transactionData.reference_number}
                  onChange={(e) =>
                    setTransactionData({
                      ...transactionData,
                      reference_number: e.target.value,
                    })
                  }
                  required
                />
              </Grid>
              {transactionType === 'TRANSFER' && (
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    select
                    label="Destination Warehouse"
                    value={transactionData.destination_warehouse_id}
                    onChange={(e) =>
                      setTransactionData({
                        ...transactionData,
                        destination_warehouse_id: e.target.value,
                      })
                    }
                    required
                  >
                    {(warehouses || [])
                      .filter((w: any) => w.id !== selectedItem?.warehouse.id)
                      .map((warehouse: any) => (
                        <MenuItem key={warehouse.id} value={warehouse.id}>
                          {warehouse.name}
                        </MenuItem>
                      ))}
                  </TextField>
                </Grid>
              )}
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  label="Notes"
                  value={transactionData.notes}
                  onChange={(e) =>
                    setTransactionData({
                      ...transactionData,
                      notes: e.target.value,
                    })
                  }
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseTransactionDialog}>Cancel</Button>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={transactionMutation.isLoading}
            >
              Submit
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && <Box>{children}</Box>}
    </div>
  );
}

export default InventoryItems;
