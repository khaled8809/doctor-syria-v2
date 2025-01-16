import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  CircularProgress,
  Alert,
  useTheme,
} from '@mui/material';
import { usePatientContext } from '../../contexts/PatientContext';
import { useAIService } from '../../services/ai-service';

interface HealthRisk {
  riskType: string;
  riskLevel: 'low' | 'medium' | 'high';
  probability: number;
  factors: string[];
  recommendations: string[];
}

interface HealthMetric {
  name: string;
  value: number;
  unit: string;
  status: 'normal' | 'warning' | 'critical';
  trend: 'up' | 'down' | 'stable';
}

export function HealthRiskPredictor() {
  const theme = useTheme();
  const { currentPatient } = usePatientContext();
  const { predictHealthRisks, getHealthMetrics } = useAIService();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [healthRisks, setHealthRisks] = useState<HealthRisk[]>([]);
  const [healthMetrics, setHealthMetrics] = useState<HealthMetric[]>([]);

  useEffect(() => {
    if (!currentPatient) return;

    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const [risks, metrics] = await Promise.all([
          predictHealthRisks(currentPatient.id),
          getHealthMetrics(currentPatient.id),
        ]);

        setHealthRisks(risks);
        setHealthMetrics(metrics);
      } catch (err) {
        setError('حدث خطأ أثناء تحليل المخاطر الصحية');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [currentPatient, predictHealthRisks, getHealthMetrics]);

  const getRiskColor = (riskLevel: HealthRisk['riskLevel']) => {
    switch (riskLevel) {
      case 'high':
        return theme.palette.error.main;
      case 'medium':
        return theme.palette.warning.main;
      case 'low':
        return theme.palette.success.main;
      default:
        return theme.palette.info.main;
    }
  };

  const getMetricColor = (status: HealthMetric['status']) => {
    switch (status) {
      case 'critical':
        return theme.palette.error.main;
      case 'warning':
        return theme.palette.warning.main;
      case 'normal':
        return theme.palette.success.main;
      default:
        return theme.palette.text.primary;
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={3}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        تحليل المخاطر الصحية
      </Typography>

      <Grid container spacing={3}>
        {healthRisks.map((risk, index) => (
          <Grid item xs={12} md={6} key={index}>
            <Paper sx={{ p: 3 }}>
              <Typography
                variant="h6"
                gutterBottom
                sx={{ color: getRiskColor(risk.riskLevel) }}
              >
                {risk.riskType}
              </Typography>

              <Box sx={{ mb: 2 }}>
                <Typography variant="body1" gutterBottom>
                  مستوى الخطورة: {risk.riskLevel}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  احتمالية: {Math.round(risk.probability * 100)}%
                </Typography>
              </Box>

              <Typography variant="subtitle1" gutterBottom>
                العوامل المؤثرة:
              </Typography>
              <ul>
                {risk.factors.map((factor, idx) => (
                  <li key={idx}>{factor}</li>
                ))}
              </ul>

              <Typography variant="subtitle1" gutterBottom>
                التوصيات:
              </Typography>
              <ul>
                {risk.recommendations.map((rec, idx) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            </Paper>
          </Grid>
        ))}

        {healthMetrics.map((metric, index) => (
          <Grid item xs={12} md={4} key={index}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                {metric.name}
              </Typography>
              <Typography
                variant="h4"
                sx={{ color: getMetricColor(metric.status) }}
              >
                {metric.value}
                <Typography component="span" variant="body1">
                  {metric.unit}
                </Typography>
              </Typography>
              <Typography
                variant="body2"
                color="text.secondary"
                sx={{ mt: 1 }}
              >
                الحالة: {metric.status}
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default HealthRiskPredictor;
