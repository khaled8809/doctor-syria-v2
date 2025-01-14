import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Chip,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Warning,
  Info,
  Timeline,
  Assessment,
  Psychology,
  Analytics,
  BarChart,
  BubbleChart
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

interface Prediction {
  id: string;
  category: string;
  metric: string;
  currentValue: number;
  predictedValue: number;
  confidence: number;
  trend: 'up' | 'down' | 'stable';
  timeframe: string;
  impactLevel: 'high' | 'medium' | 'low';
  recommendations: string[];
  historicalData: any[];
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

export const AIPredictions: React.FC = () => {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [selectedPrediction, setSelectedPrediction] = useState<Prediction | null>(null);
  const [detailsDialog, setDetailsDialog] = useState(false);
  const [aiMetrics, setAiMetrics] = useState({
    accuracy: 0,
    coverage: 0,
    alerts: 0
  });

  useEffect(() => {
    // تحميل البيانات الأولية
    fetchPredictions();
  }, []);

  const fetchPredictions = async () => {
    // API calls to fetch AI predictions
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up':
        return <TrendingUp color="success" />;
      case 'down':
        return <TrendingDown color="error" />;
      default:
        return <Timeline color="info" />;
    }
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      default:
        return 'info';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">التنبؤات الذكية</Typography>
        <Box>
          <Button
            variant="outlined"
            startIcon={<Psychology />}
            sx={{ mr: 1 }}
          >
            تدريب النموذج
          </Button>
          <Button
            variant="contained"
            startIcon={<Analytics />}
          >
            تحليل متقدم
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* AI Metrics */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                دقة التنبؤات
              </Typography>
              <Typography variant="h4">
                {aiMetrics.accuracy}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={aiMetrics.accuracy}
                color="primary"
                sx={{ mt: 2 }}
              />
              <Typography variant="caption" color="text.secondary">
                متوسط الدقة خلال آخر 30 يوم
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                تغطية البيانات
              </Typography>
              <Typography variant="h4">
                {aiMetrics.coverage}%
              </Typography>
              <Box sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
                <BubbleChart color="primary" />
                <Typography variant="body2" sx={{ ml: 1 }}>
                  نسبة البيانات المحللة
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                التنبيهات النشطة
              </Typography>
              <Typography variant="h4" color="warning.main">
                {aiMetrics.alerts}
              </Typography>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<Warning />}
                sx={{ mt: 2 }}
                color="warning"
              >
                عرض التنبيهات
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Predictions Table */}
        <Grid item xs={12}>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>المؤشر</TableCell>
                  <TableCell>القيمة الحالية</TableCell>
                  <TableCell>التنبؤ</TableCell>
                  <TableCell>الثقة</TableCell>
                  <TableCell>الاتجاه</TableCell>
                  <TableCell>التأثير</TableCell>
                  <TableCell>التوصيات</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {predictions.map((prediction) => (
                  <TableRow
                    key={prediction.id}
                    onClick={() => {
                      setSelectedPrediction(prediction);
                      setDetailsDialog(true);
                    }}
                    sx={{ cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}
                  >
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <BarChart sx={{ mr: 1 }} />
                        <Box>
                          <Typography variant="body1">
                            {prediction.metric}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {prediction.category}
                          </Typography>
                        </Box>
                      </Box>
                    </TableCell>
                    <TableCell>{prediction.currentValue}</TableCell>
                    <TableCell>
                      <Typography
                        color={prediction.predictedValue > prediction.currentValue ? 'success.main' : 'error.main'}
                      >
                        {prediction.predictedValue}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <LinearProgress
                          variant="determinate"
                          value={prediction.confidence}
                          sx={{ width: 100, mr: 1 }}
                        />
                        {prediction.confidence}%
                      </Box>
                    </TableCell>
                    <TableCell>
                      {getTrendIcon(prediction.trend)}
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={prediction.impactLevel}
                        color={getImpactColor(prediction.impactLevel)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Tooltip title={prediction.recommendations.join('\n')}>
                        <IconButton size="small">
                          <Info />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>
      </Grid>

      {/* Prediction Details Dialog */}
      <Dialog
        open={detailsDialog}
        onClose={() => setDetailsDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          تفاصيل التنبؤ - {selectedPrediction?.metric}
        </DialogTitle>
        <DialogContent>
          {selectedPrediction && (
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={selectedPrediction.historicalData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <RechartsTooltip />
                    <Line
                      type="monotone"
                      dataKey="value"
                      stroke="#8884d8"
                      name="القيمة الفعلية"
                    />
                    <Line
                      type="monotone"
                      dataKey="prediction"
                      stroke="#82ca9d"
                      name="التنبؤ"
                      strokeDasharray="5 5"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  التوصيات
                </Typography>
                {selectedPrediction.recommendations.map((rec, index) => (
                  <Typography key={index} variant="body2" sx={{ mb: 1 }}>
                    • {rec}
                  </Typography>
                ))}
              </Grid>
            </Grid>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDetailsDialog(false)}>إغلاق</Button>
          <Button variant="contained" color="primary">
            تصدير التحليل
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AIPredictions;
