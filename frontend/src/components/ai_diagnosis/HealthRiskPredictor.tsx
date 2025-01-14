import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
  Tooltip,
  IconButton,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  InfoOutlined,
  TrendingUp,
  TrendingDown,
  Warning,
  CheckCircle,
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
  Tooltip as RechartsTooltip,
} from 'recharts';
import { useAIService } from '../../services/ai-service';
import { useTheme } from '@mui/material/styles';

interface RiskFactor {
  name: string;
  probability: number;
  trend: 'up' | 'down' | 'stable';
  severity: 'low' | 'medium' | 'high';
  description: string;
}

interface HealthMetric {
  name: string;
  current: number;
  target: number;
  unit: string;
  status: 'good' | 'warning' | 'critical';
}

export default function HealthRiskPredictor({ patientId }: { patientId: number }) {
  const theme = useTheme();
  const { predictPatientRisks } = useAIService();
  const [loading, setLoading] = useState(true);
  const [riskFactors, setRiskFactors] = useState<RiskFactor[]>([]);
  const [healthMetrics, setHealthMetrics] = useState<HealthMetric[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadPredictions = async () => {
      try {
        const data = await predictPatientRisks(patientId);
        setRiskFactors(data.riskFactors);
        setHealthMetrics(data.healthMetrics);
      } catch (err) {
        setError('حدث خطأ في تحميل التنبؤات');
      } finally {
        setLoading(false);
      }
    };

    loadPredictions();
  }, [patientId]);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return theme.palette.error.main;
      case 'medium':
        return theme.palette.warning.main;
      default:
        return theme.palette.success.main;
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up':
        return <TrendingUp color="error" />;
      case 'down':
        return <TrendingDown color="success" />;
      default:
        return null;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'critical':
        return <Warning color="error" />;
      case 'warning':
        return <Warning color="warning" />;
      default:
        return <CheckCircle color="success" />;
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h6" gutterBottom>
        تحليل المخاطر الصحية
      </Typography>

      <Grid container spacing={3}>
        {/* عوامل الخطر */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="subtitle1" gutterBottom>
                عوامل الخطر المحتملة
              </Typography>

              {riskFactors.map((factor, index) => (
                <Box
                  key={index}
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    mb: 2,
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography>{factor.name}</Typography>
                    <Tooltip title={factor.description}>
                      <IconButton size="small">
                        <InfoOutlined fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Chip
                      label={`${Math.round(factor.probability * 100)}%`}
                      size="small"
                      sx={{
                        bgcolor: getSeverityColor(factor.severity),
                        color: 'white',
                      }}
                    />
                    {getTrendIcon(factor.trend)}
                  </Box>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>

        {/* المؤشرات الصحية */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="subtitle1" gutterBottom>
                المؤشرات الصحية
              </Typography>

              {healthMetrics.map((metric, index) => (
                <Box key={index} sx={{ mb: 3 }}>
                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      mb: 1,
                    }}
                  >
                    <Typography variant="body2">
                      {metric.name} ({metric.unit})
                    </Typography>
                    {getStatusIcon(metric.status)}
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Box sx={{ flexGrow: 1 }}>
                      <LinearProgress
                        variant="determinate"
                        value={(metric.current / metric.target) * 100}
                        color={
                          metric.status === 'good'
                            ? 'success'
                            : metric.status === 'warning'
                            ? 'warning'
                            : 'error'
                        }
                      />
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {metric.current}/{metric.target}
                    </Typography>
                  </Box>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>

        {/* رسم بياني للاتجاهات */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="subtitle1" gutterBottom>
                تحليل الاتجاهات
              </Typography>

              <Box sx={{ height: 300 }}>
                <ResponsiveContainer>
                  <BarChart
                    data={riskFactors}
                    margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <RechartsTooltip />
                    <Legend />
                    <Bar
                      dataKey="probability"
                      name="احتمالية الخطر"
                      fill={theme.palette.primary.main}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
