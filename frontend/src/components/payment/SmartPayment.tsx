import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Alert,
  Stepper,
  Step,
  StepLabel,
  CircularProgress,
} from '@mui/material';
import {
  CreditCard,
  AccountBalance,
  LocalAtm,
  Receipt,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  CardGiftcard,
  Timeline,
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';

interface PaymentMethod {
  id: string;
  type: 'card' | 'bank' | 'cash';
  name: string;
  details: string;
  isDefault: boolean;
}

interface Bill {
  id: string;
  date: string;
  amount: number;
  description: string;
  status: 'pending' | 'paid' | 'overdue';
  dueDate: string;
}

interface InsuranceClaim {
  id: string;
  date: string;
  amount: number;
  status: 'pending' | 'approved' | 'rejected';
  serviceType: string;
}

const SmartPayment: React.FC = () => {
  const { t } = useTranslation();
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([]);
  const [bills, setBills] = useState<Bill[]>([]);
  const [insuranceClaims, setInsuranceClaims] = useState<InsuranceClaim[]>([]);
  const [openAddPayment, setOpenAddPayment] = useState(false);
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [loyaltyPoints, setLoyaltyPoints] = useState(0);

  useEffect(() => {
    // Fetch payment data
    fetchPaymentData();
  }, []);

  const fetchPaymentData = async () => {
    // This would be replaced with actual API calls
    const mockPaymentMethods: PaymentMethod[] = [
      {
        id: '1',
        type: 'card',
        name: 'Visa ****1234',
        details: 'Expires 12/25',
        isDefault: true,
      },
    ];

    const mockBills: Bill[] = [
      {
        id: '1',
        date: '2025-01-05',
        amount: 150,
        description: 'استشارة طبية',
        status: 'pending',
        dueDate: '2025-01-20',
      },
    ];

    const mockInsuranceClaims: InsuranceClaim[] = [
      {
        id: '1',
        date: '2025-01-01',
        amount: 300,
        status: 'approved',
        serviceType: 'فحص مخبري',
      },
    ];

    setPaymentMethods(mockPaymentMethods);
    setBills(mockBills);
    setInsuranceClaims(mockInsuranceClaims);
    setLoyaltyPoints(150);
  };

  const handlePayment = async (billId: string) => {
    setLoading(true);
    try {
      // Process payment
      await new Promise(resolve => setTimeout(resolve, 2000));
      setBills(prev =>
        prev.map(bill =>
          bill.id === billId ? { ...bill, status: 'paid' } : bill
        )
      );
      // Add loyalty points
      setLoyaltyPoints(prev => prev + 10);
    } catch (error) {
      console.error('Payment error:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderPaymentMethods = () => (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">{t('payment.methods.title')}</Typography>
        <Button
          startIcon={<AddIcon />}
          variant="contained"
          onClick={() => setOpenAddPayment(true)}
        >
          {t('payment.methods.add')}
        </Button>
      </Box>
      <Grid container spacing={3}>
        {paymentMethods.map(method => (
          <Grid item xs={12} sm={6} md={4} key={method.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  {method.type === 'card' && <CreditCard sx={{ mr: 1 }} />}
                  {method.type === 'bank' && <AccountBalance sx={{ mr: 1 }} />}
                  {method.type === 'cash' && <LocalAtm sx={{ mr: 1 }} />}
                  <Typography variant="h6">{method.name}</Typography>
                </Box>
                <Typography color="textSecondary">{method.details}</Typography>
                {method.isDefault && (
                  <Chip
                    label={t('payment.methods.default')}
                    color="primary"
                    size="small"
                    sx={{ mt: 1 }}
                  />
                )}
              </CardContent>
              <CardActions>
                <Button size="small" startIcon={<EditIcon />}>
                  {t('common.edit')}
                </Button>
                <Button size="small" startIcon={<DeleteIcon />} color="error">
                  {t('common.delete')}
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Paper>
  );

  const renderBills = () => (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        {t('payment.bills.title')}
      </Typography>
      <List>
        {bills.map(bill => (
          <ListItem key={bill.id}>
            <ListItemText
              primary={
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Typography variant="subtitle1">
                    {bill.description}
                  </Typography>
                  <Chip
                    label={t(`payment.bills.status.${bill.status}`)}
                    color={
                      bill.status === 'paid'
                        ? 'success'
                        : bill.status === 'overdue'
                        ? 'error'
                        : 'warning'
                    }
                    size="small"
                    sx={{ ml: 1 }}
                  />
                </Box>
              }
              secondary={`${bill.amount} ${t('payment.currency')} - ${t('payment.bills.due')} ${bill.dueDate}`}
            />
            <ListItemSecondaryAction>
              {bill.status === 'pending' && (
                <Button
                  variant="contained"
                  size="small"
                  onClick={() => handlePayment(bill.id)}
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={24} /> : t('payment.bills.pay')}
                </Button>
              )}
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>
    </Paper>
  );

  const renderInsuranceClaims = () => (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        {t('payment.insurance.title')}
      </Typography>
      <List>
        {insuranceClaims.map(claim => (
          <ListItem key={claim.id}>
            <ListItemText
              primary={
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Typography variant="subtitle1">
                    {claim.serviceType}
                  </Typography>
                  <Chip
                    label={t(`payment.insurance.status.${claim.status}`)}
                    color={
                      claim.status === 'approved'
                        ? 'success'
                        : claim.status === 'rejected'
                        ? 'error'
                        : 'warning'
                    }
                    size="small"
                    sx={{ ml: 1 }}
                  />
                </Box>
              }
              secondary={`${claim.amount} ${t('payment.currency')} - ${claim.date}`}
            />
          </ListItem>
        ))}
      </List>
    </Paper>
  );

  const renderLoyaltyProgram = () => (
    <Paper sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <CardGiftcard sx={{ mr: 1 }} />
        <Typography variant="h6">{t('payment.loyalty.title')}</Typography>
      </Box>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6}>
          <Card>
            <CardContent>
              <Typography variant="h4" gutterBottom>
                {loyaltyPoints}
              </Typography>
              <Typography color="textSecondary">
                {t('payment.loyalty.points')}
              </Typography>
              <Button
                variant="outlined"
                startIcon={<Timeline />}
                sx={{ mt: 2 }}
              >
                {t('payment.loyalty.history')}
              </Button>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {t('payment.loyalty.rewards')}
              </Typography>
              <List>
                <ListItem>
                  <ListItemText
                    primary="خصم 10%"
                    secondary="200 نقطة"
                  />
                  <Button variant="outlined" disabled={loyaltyPoints < 200}>
                    {t('payment.loyalty.redeem')}
                  </Button>
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="استشارة مجانية"
                    secondary="500 نقطة"
                  />
                  <Button variant="outlined" disabled={loyaltyPoints < 500}>
                    {t('payment.loyalty.redeem')}
                  </Button>
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Paper>
  );

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          {t('payment.title')}
        </Typography>

        {renderPaymentMethods()}
        {renderBills()}
        {renderInsuranceClaims()}
        {renderLoyaltyProgram()}

        {/* Add Payment Method Dialog */}
        <Dialog
          open={openAddPayment}
          onClose={() => setOpenAddPayment(false)}
          maxWidth="sm"
          fullWidth
        >
          <DialogTitle>{t('payment.methods.add')}</DialogTitle>
          <DialogContent>
            <Stepper activeStep={activeStep} sx={{ py: 3 }}>
              <Step>
                <StepLabel>{t('payment.methods.steps.type')}</StepLabel>
              </Step>
              <Step>
                <StepLabel>{t('payment.methods.steps.details')}</StepLabel>
              </Step>
              <Step>
                <StepLabel>{t('payment.methods.steps.confirm')}</StepLabel>
              </Step>
            </Stepper>
            {/* Add payment method form would go here */}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenAddPayment(false)}>
              {t('common.cancel')}
            </Button>
            <Button
              variant="contained"
              onClick={() => {
                if (activeStep === 2) {
                  setOpenAddPayment(false);
                  setActiveStep(0);
                } else {
                  setActiveStep(prev => prev + 1);
                }
              }}
            >
              {activeStep === 2 ? t('common.finish') : t('common.next')}
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </Container>
  );
};

export default SmartPayment;
