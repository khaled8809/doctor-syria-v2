import React, { useState } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Button,
  Tab,
  Tabs,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
} from '@mui/material';
import {
  Timeline,
  TrendingUp,
  LocalHospital,
  Warning,
  Assessment,
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import axios from 'axios';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

interface AdmissionPrediction {
  date: string;
  predicted: number;
  actual?: number;
  confidence: {
    lower: number;
    upper: number;
  };
}

interface ResourcePrediction {
  productId: number;
  productName: string;
  currentStock: number;
  predictedNeed: number;
  confidence: number;
  reorderPoint: number;
}

interface EmergencyPattern {
  type: string;
  count: number;
  trend: 'increasing' | 'decreasing' | 'stable';
  peak_hours: string[];
}

interface EfficiencyMetric {
  name: string;
  value: number;
  target: number;
  trend: 'up' | 'down' | 'stable';
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const AnalyticsDashboard = () => {
  const [selectedTab, setSelectedTab] = useState(0);

  // Fetch analytics data
  const { data: admissionPredictions, isLoading: loadingAdmissions } = useQuery<
    AdmissionPrediction[]
  >('admission-predictions', () =>
    axios.get('/api/analytics/admissions/').then((res) => res.data)
  );

  const { data: resourcePredictions, isLoading: loadingResources } = useQuery<
    ResourcePrediction[]
  >('resource-predictions', () =>
    axios.get('/api/analytics/resources/').then((res) => res.data)
  );

  const { data: emergencyPatterns, isLoading: loadingPatterns } = useQuery<
    EmergencyPattern[]
  >('emergency-patterns', () =>
    axios.get('/api/analytics/emergencies/').then((res) => res.data)
  );

  const { data: efficiencyMetrics, isLoading: loadingMetrics } = useQuery<
    EfficiencyMetric[]
  >('efficiency-metrics', () =>
    axios.get('/api/analytics/efficiency/').then((res) => res.data)
  );

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setSelectedTab(newValue);
  };

  const renderAdmissionPredictions = () => (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Admission Predictions (Next 7 Days)
          </Typography>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={admissionPredictions}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="predicted"
                stroke="#8884d8"
                name="Predicted"
              />
              <Line
                type="monotone"
                dataKey="actual"
                stroke="#82ca9d"
                name="Actual"
              />
            </LineChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>
    </Grid>
  );

  const renderResourcePredictions = () => (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Resource Predictions
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Product</TableCell>
                  <TableCell align="right">Current Stock</TableCell>
                  <TableCell align="right">Predicted Need</TableCell>
                  <TableCell align="right">Confidence</TableCell>
                  <TableCell>Status</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {resourcePredictions?.map((item) => (
                  <TableRow key={item.productId}>
                    <TableCell>{item.productName}</TableCell>
                    <TableCell align="right">{item.currentStock}</TableCell>
                    <TableCell align="right">{item.predictedNeed}</TableCell>
                    <TableCell align="right">{item.confidence}%</TableCell>
                    <TableCell>
                      {item.currentStock < item.reorderPoint ? (
                        <Typography color="error">Reorder Required</Typography>
                      ) : (
                        <Typography color="success">Adequate</Typography>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </Grid>
    </Grid>
  );

  const renderEmergencyPatterns = () => (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Emergency Types Distribution
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={emergencyPatterns}
                dataKey="count"
                nameKey="type"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label
              >
                {emergencyPatterns?.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Peak Hours Analysis
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={emergencyPatterns}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="type" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>
    </Grid>
  );

  const renderEfficiencyMetrics = () => (
    <Grid container spacing={3}>
      {efficiencyMetrics?.map((metric) => (
        <Grid item xs={12} md={3} key={metric.name}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                {metric.name}
              </Typography>
              <Box display="flex" alignItems="center">
                <Typography variant="h4" component="div">
                  {metric.value}
                </Typography>
                <Box ml={1}>
                  {metric.trend === 'up' ? (
                    <TrendingUp color="success" />
                  ) : metric.trend === 'down' ? (
                    <TrendingUp color="error" sx={{ transform: 'rotate(180deg)' }} />
                  ) : (
                    <Timeline color="primary" />
                  )}
                </Box>
              </Box>
              <Typography variant="body2" color="textSecondary">
                Target: {metric.target}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );

  if (
    loadingAdmissions ||
    loadingResources ||
    loadingPatterns ||
    loadingMetrics
  ) {
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
            <Typography variant="h4">Analytics Dashboard</Typography>
            <Button
              variant="contained"
              startIcon={<Assessment />}
              onClick={() => {
                // Generate report logic
              }}
            >
              Generate Report
            </Button>
          </Box>
        </Grid>

        {/* Tabs */}
        <Grid item xs={12}>
          <Paper sx={{ width: '100%' }}>
            <Tabs
              value={selectedTab}
              onChange={handleTabChange}
              variant="fullWidth"
            >
              <Tab
                icon={<LocalHospital />}
                label="Admission Predictions"
                id="tab-0"
              />
              <Tab
                icon={<TrendingUp />}
                label="Resource Predictions"
                id="tab-1"
              />
              <Tab icon={<Warning />} label="Emergency Patterns" id="tab-2" />
              <Tab
                icon={<Assessment />}
                label="Efficiency Metrics"
                id="tab-3"
              />
            </Tabs>
          </Paper>
        </Grid>

        {/* Tab Panels */}
        <Grid item xs={12}>
          {selectedTab === 0 && renderAdmissionPredictions()}
          {selectedTab === 1 && renderResourcePredictions()}
          {selectedTab === 2 && renderEmergencyPatterns()}
          {selectedTab === 3 && renderEfficiencyMetrics()}
        </Grid>
      </Grid>
    </Box>
  );
};

export default AnalyticsDashboard;
