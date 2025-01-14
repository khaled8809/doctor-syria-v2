import { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
  Button,
  useTheme,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAppSelector } from '../../store';
import { api } from '../../store/api';

interface TenantData {
  id: string;
  name: string;
  subscription: {
    plan: string;
    status: string;
    expiryDate: string;
  };
  usage: {
    storage: number;
    bandwidth: number;
    users: number;
  };
  billing: {
    nextBillingDate: string;
    amount: number;
    currency: string;
  };
}

const TenantDashboard = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const [tenantData, setTenantData] = useState<TenantData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { user } = useAppSelector((state) => state.auth);

  useEffect(() => {
    const fetchTenantData = async () => {
      try {
        const response = await api.get<TenantData>('/api/tenant');
        setTenantData(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to load tenant data');
        console.error('Error fetching tenant data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTenantData();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" flexDirection="column" alignItems="center" minHeight="400px" p={3}>
        <Typography color="error" gutterBottom>
          {error}
        </Typography>
        <Button variant="contained" onClick={() => window.location.reload()}>
          Retry
        </Button>
      </Box>
    );
  }

  if (!tenantData) {
    return null;
  }

  const { subscription, usage, billing } = tenantData;

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Tenant Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Subscription Info */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Subscription
              </Typography>
              <Typography variant="body1">
                Plan: {subscription.plan}
              </Typography>
              <Typography variant="body1">
                Status: {subscription.status}
              </Typography>
              <Typography variant="body1">
                Expires: {new Date(subscription.expiryDate).toLocaleDateString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Usage Stats */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Usage
              </Typography>
              <Typography variant="body1">
                Storage: {usage.storage}GB
              </Typography>
              <Typography variant="body1">
                Bandwidth: {usage.bandwidth}GB
              </Typography>
              <Typography variant="body1">
                Users: {usage.users}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Billing Info */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Billing
              </Typography>
              <Typography variant="body1">
                Next Billing: {new Date(billing.nextBillingDate).toLocaleDateString()}
              </Typography>
              <Typography variant="body1">
                Amount: {billing.amount} {billing.currency}
              </Typography>
              <Button
                variant="contained"
                color="primary"
                onClick={() => navigate('/billing')}
                sx={{ mt: 2 }}
              >
                Manage Billing
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default TenantDashboard;
